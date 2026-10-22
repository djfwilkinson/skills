#!/usr/bin/env python3
"""Device-level action ledger for orchestrated runs. Python 3.9+, stdlib only.

  python3 ledger.py                          start the ledger and print its URL
  python3 ledger.py register <run-dir> [name]  list a run, then start the ledger
  python3 ledger.py complete <run-dir>       archive a completed run
  python3 ledger.py serve                    run the server in the foreground

Starting creates the ledger directory, replaces its index when the template's
ledger-version is newer, and starts the server unless the same or a newer
version is running. A registered run is runs/<key>.json holding run.dir. The
server derives each run's asks from ticket YAML and ask pages under run.dir,
returns them at /runs, serves files under run.dir (including asks/, tickets/,
and mocks/) at /r/<key>/<path>, and serves read-only target-project files at
/r/<key>/project/<path> so run-local mocks in mocks/ can load production CSS
and assets. It keeps registrations whose run directory is unavailable and
flags looksComplete when every goal in GOALS.md is achieved or abandoned and no ask is open. POST
/r/<key>/complete with header X-Action-Ledger: complete archives such a run's
registration so its tickets and ask pages remain served; the custom header
keeps other sites from sending it. For each
presented ask, the server also reports as checks the tickets named in its
may_withdraw_on that are not resolved or cancelled (status null when unreadable).
"""
import json, mimetypes, os, re, shutil, signal, socket, subprocess, sys, tempfile, time, urllib.request
from contextlib import contextmanager
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

HOME = Path(os.environ.get("ACTION_LEDGER_HOME") or Path.home() / ".agent-runs" / "action-ledger")
RUNS, PORT_FILE, PID_FILE, INDEX = HOME / "runs", HOME / "port", HOME / "pid", HOME / "index.html"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "ask-index.html"
FIRST_PORT, PORT_TRIES, VERSION = 47391, 20, 11
NAME = f"action-ledger/{VERSION}"
UNSETTLED = ("proposed", "ready", "active", "blocked")
ARCHIVE_CACHE = {}


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return None


def read_json_with_bytes(path):
    try:
        raw = path.read_bytes()
        return raw, json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, ValueError):
        return None, None


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            json.dump(data, file)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def registration_lock(path):
    lock = path.with_suffix(f"{path.suffix}.lock")
    descriptor = None
    for _ in range(100):
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > 30:
                    lock.unlink()
                    continue
            except OSError:
                continue
            time.sleep(0.05)
    if descriptor is None:
        raise TimeoutError(f"registration lock unavailable: {path.name}")
    try:
        yield
    finally:
        os.close(descriptor)
        lock.unlink(missing_ok=True)


def ticket_yaml(path):
    try:
        with path.open(encoding="utf-8") as file:
            head = file.read(2000).split("---", 2)
    except (OSError, UnicodeError):
        return {}
    if len(head) < 3 or head[0].strip():
        return {}
    return {key: value.strip().strip("\"'") for key, value in re.findall(r"(?m)^(\w+):[ \t]*(.*)$", head[1])}


def page_value(page, key):
    found = re.search(rf'(?<![\w.])["\']?{key}["\']?\s*:\s*("(?:[^"\\\n]|\\.)*")', page)
    try:
        return json.loads(found[1]) if found else ""
    except ValueError:
        return ""


def goal_statuses(base):
    try:
        return re.findall(r"(?m)^### Status[ \t]*\n+[ \t]*(\w+)", (base / "GOALS.md").read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return []


def archive_stamp(base):
    paths = [base / "GOALS.md", *(base / "tickets").glob("*.md"), *(base / "asks").glob("*.html")]
    stamp = []
    for path in paths:
        try:
            stat = path.stat()
        except OSError:
            continue
        stamp.append((str(path), stat.st_mtime_ns, stat.st_size))
    return tuple(stamp)


def link_ids(raw):
    if raw is None or raw in ("[]", "null"):
        return []
    if not (raw.startswith("[") and raw.endswith("]")):
        return None
    items = (item.strip().strip("\"'") for item in raw[1:-1].split(","))
    return list(dict.fromkeys(item for item in items if item))


def checks(ask_id, raw, metas):
    refs = link_ids(raw)
    if refs is None:
        return [{"id": raw or "may_withdraw_on", "title": "", "status": None}]
    found = []
    for ref in refs:
        meta = metas.get(ref) if ref != ask_id else None
        human = meta is not None and meta.get("presentation") not in (None, "", "null")
        status = None if meta is None or human else meta.get("status")
        if status in ("resolved", "cancelled"):
            continue
        found.append({"id": ref, "title": (meta or {}).get("title") or (meta or {}).get("type") or "",
                      "status": status if status in UNSETTLED else None})
    return found


def run_view(key, data):
    run = dict(data.get("run") or {}) if isinstance(data, dict) else {}
    base, asks, history, updated, metas = Path(run.get("dir") or "/nonexistent"), [], [], 0, {}
    if not base.is_dir():
        run["dirMissing"] = True
        run["looksComplete"] = False
        return {"key": key, "run": run, "asks": [], "history": []}
    cache_key = (key, run.get("archivedAt"), archive_stamp(base))
    if run.get("archivedAt") and cache_key in ARCHIVE_CACHE:
        return ARCHIVE_CACHE[cache_key]
    cacheable = True
    for path in sorted((base / "tickets").glob("*.md")):
        try:
            updated = max(updated, path.stat().st_mtime)
        except OSError:
            continue
        metas[path.stem] = ticket_yaml(path)
    for stem, meta in metas.items():
        presentation = meta.get("presentation")
        if presentation in (None, "", "null"):
            continue
        current = presentation in ("presented", "upcoming") and meta.get("status") not in ("resolved", "cancelled")
        historical = presentation in ("answered", "withdrawn")
        if not current and not historical and not run.get("archivedAt"):
            continue
        try:
            page = (base / "asks" / f"{stem}.html").read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            page = ""
            cacheable = False
        item = {"id": stem, "type": meta.get("type"), "presentation": presentation,
                "action": page_value(page, "summary") or meta.get("title"),
                "reason": page_value(page, "why"), "presentedAt": page_value(page, "presentedAt"),
                "hasPage": bool(page)}
        if run.get("archivedAt") or historical:
            history.append(item)
        if current:
            asks.append({**item, "checks": checks(stem, meta.get("may_withdraw_on"), metas) if presentation == "presented" else []})
    if updated:
        run["updatedAt"] = datetime.fromtimestamp(updated).astimezone().isoformat()
    statuses = goal_statuses(base)
    run["looksComplete"] = bool(statuses) and not asks and set(statuses) <= {"achieved", "abandoned"}
    view = {"key": key, "run": run, "asks": asks, "history": history}
    if run.get("archivedAt") and cacheable:
        for old in [entry for entry in ARCHIVE_CACHE if entry[0] == key]:
            ARCHIVE_CACHE.pop(old, None)
        ARCHIVE_CACHE[cache_key] = view
    return view


class Handler(BaseHTTPRequestHandler):
    server_version = NAME

    def local(self):
        return self.headers.get("Host", "").rsplit(":", 1)[0] in ("127.0.0.1", "localhost")

    def do_POST(self):
        parts = unquote(urlsplit(self.path).path).split("/")
        if not self.local() or self.headers.get("X-Action-Ledger") != "complete" or len(parts) != 4 or parts[1::2] != ["r", "complete"]:
            return self.send_error(403)
        path = RUNS / f"{parts[2]}.json"
        try:
            with registration_lock(path):
                raw, data = read_json_with_bytes(path)
                if not isinstance(data, dict) or not isinstance(data.get("run"), dict) or not data["run"].get("dir"):
                    return self.send_error(409, "Run registration is unreadable")
                view = run_view(parts[2], data)
                if not (view and (view["run"]["looksComplete"] or view["run"].get("dirMissing"))):
                    return self.send_error(409, "Run does not look complete")
                run = dict(data.get("run") or {})
                run["archivedAt"] = datetime.now().astimezone().isoformat()
                try:
                    if path.read_bytes() != raw:
                        return self.send_error(409, "Run registration changed")
                except OSError:
                    return self.send_error(409, "Run registration changed")
                write_json(path, {"run": run})
        except TimeoutError:
            return self.send_error(409, "Run registration is busy")
        self.send(b"{}", "application/json")

    def do_GET(self):
        if not self.local():
            return self.send_error(403)
        path = unquote(urlsplit(self.path).path)
        if path == "/":
            return self.send(INDEX.read_bytes(), "text/html")
        if path == "/runs":
            views = [run_view(file.stem, read_json(file)) for file in sorted(RUNS.glob("*.json"))]
            return self.send(json.dumps([view for view in views if view]).encode(), "application/json")
        parts = path.split("/", 3)
        if len(parts) == 4 and parts[1] == "r":
            run = read_json(RUNS / f"{parts[2]}.json") or {}
            base = Path(run.get("run", {}).get("dir") or "/nonexistent").resolve()
            if parts[3].startswith("project/"):
                proj = next((p.parent for p in base.parents if p.name == ".agent-runs"), None)
                rel = parts[3][len("project/"):]
                file = (proj / rel).resolve() if proj else Path("/nonexistent")
                if proj and file.is_relative_to(proj.resolve()) and file.is_file() and not any(
                    part.startswith(".env") or part in (".git", ".agent-runs") for part in file.relative_to(proj.resolve()).parts
                ):
                    kind = mimetypes.guess_type(file.name)[0] or "text/plain"
                    return self.send(file.read_bytes(), "text/plain" if kind == "text/markdown" else kind)
            file = (base / parts[3]).resolve()
            if file.is_relative_to(base) and file.is_file():
                kind = mimetypes.guess_type(file.name)[0] or "text/plain"
                return self.send(file.read_bytes(), "text/plain" if kind == "text/markdown" else kind)
        self.send_error(404)

    def send(self, body, kind):
        self.send_response(200)
        self.send_header("Content-Type", f"{kind}; charset=utf-8" if kind.startswith("text/") else kind)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class Server(ThreadingHTTPServer):
    allow_reuse_address = os.name != "nt"


def taken(port):
    try:
        socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
        return True
    except OSError:
        return False


def saved_port():
    try:
        return int(PORT_FILE.read_text())
    except (OSError, ValueError):
        return None


def running_version():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{saved_port()}/runs", timeout=1) as reply:
            found = re.match(r"action-ledger/(\d+)", reply.headers.get("Server", ""))
            return int(found[1]) if found else None
    except Exception:
        return None


def wait_for(ready):
    for _ in range(50):
        if ready():
            return True
        time.sleep(0.1)
    return False


def serve():
    for port in dict.fromkeys(filter(None, [saved_port(), *range(FIRST_PORT, FIRST_PORT + PORT_TRIES)])):
        if taken(port):
            continue
        try:
            server = Server(("127.0.0.1", port), Handler)
        except OSError:
            continue
        PORT_FILE.write_text(str(port))
        PID_FILE.write_text(str(os.getpid()))
        server.serve_forever()
    sys.exit(f"{NAME}: no free port from {FIRST_PORT} to {FIRST_PORT + PORT_TRIES - 1}")


def page_version(path):
    try:
        found = re.search(r'name="ledger-version" content="(\d+)"', path.read_text(encoding="utf-8"))
    except OSError:
        return -1
    return int(found[1]) if found else 0


def install_index():
    if page_version(TEMPLATE) <= page_version(INDEX):
        return
    handle, temporary = tempfile.mkstemp(prefix=".index.html.", dir=HOME)
    os.close(handle)
    try:
        shutil.copyfile(TEMPLATE, temporary)
        os.replace(temporary, INDEX)
    finally:
        Path(temporary).unlink(missing_ok=True)


def start(show_url=True):
    RUNS.mkdir(parents=True, exist_ok=True)
    running = running_version()
    if running is not None and running < VERSION:
        try:
            os.kill(int(PID_FILE.read_text()), signal.SIGTERM)
        except (OSError, ValueError):
            pass
        if not wait_for(lambda: running_version() is None):
            sys.exit(f"{NAME}: older ledger server is still running")
        running = None
    install_index()
    if running is None:
        flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        subprocess.Popen([sys.executable, __file__, "serve"], start_new_session=True, creationflags=flags,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not wait_for(lambda: running_version() is not None):
            sys.exit(f"{NAME}: server did not start")
    if show_url:
        print(f"http://127.0.0.1:{saved_port()}/")


def run_file(run_dir):
    run_dir = Path(run_dir).resolve()
    project = next((p.parent.name for p in run_dir.parents if p.name == ".agent-runs"), run_dir.parent.name)
    return run_dir, project, RUNS / f"{project}--{run_dir.name}.json"


def register(run_dir, name=None):
    run_dir, project, path = run_file(run_dir)
    start(show_url=False)
    try:
        with registration_lock(path):
            run = {"id": run_dir.name, "name": run_dir.name, "project": project, **((read_json(path) or {}).get("run") or {})}
            run.pop("archivedAt", None)
            write_json(path, {"run": {**run, **({"name": name} if name else {}), "dir": str(run_dir)}})
    except TimeoutError as error:
        sys.exit(f"{NAME}: {error}")
    print(f"http://127.0.0.1:{saved_port()}/")


def complete(run_dir):
    run_dir, project, path = run_file(run_dir)
    start(show_url=False)
    try:
        with registration_lock(path):
            raw, data = read_json_with_bytes(path)
            run = {"id": run_dir.name, "name": run_dir.name, "project": project,
                   **((data or {}).get("run") or {}), "dir": str(run_dir)}
            run["archivedAt"] = datetime.now().astimezone().isoformat()
            if raw is not None:
                try:
                    if path.read_bytes() != raw:
                        sys.exit(f"{NAME}: run registration changed while archiving")
                except OSError:
                    sys.exit(f"{NAME}: run registration changed while archiving")
            elif path.exists():
                sys.exit(f"{NAME}: run registration changed while archiving")
            write_json(path, {"run": run})
    except TimeoutError as error:
        sys.exit(f"{NAME}: {error}")


if __name__ == "__main__":
    command, *args = sys.argv[1:] or ["start"]
    {"start": start, "serve": serve, "register": register, "complete": complete}[command](*args)
