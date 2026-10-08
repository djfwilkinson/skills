#!/usr/bin/env python3
"""Device-level action ledger for orchestrated runs. Python 3.9+, stdlib only.

  python3 ledger.py                          start the ledger and print its URL
  python3 ledger.py register <run-dir> [name]  list a run, then start the ledger
  python3 ledger.py complete <run-dir>       stop listing a run
  python3 ledger.py serve                    run the server in the foreground

Starting creates the ledger directory, replaces its index when the template's
ledger-version is newer, and starts the server unless the same or a newer
version is running. A registered run is runs/<key>.json holding run.dir. The
server derives each run's asks from ticket YAML and ask pages under run.dir,
returns them at /runs, and serves files under run.dir at /r/<key>/<path>. It
skips runs whose directory is gone and flags looksComplete when every goal in
GOALS.md is achieved or abandoned and no ask is open. POST /r/<key>/complete
with header X-Action-Ledger: complete removes such a run's registration; the
custom header keeps other sites from sending it.
"""
import json, mimetypes, os, re, shutil, signal, socket, subprocess, sys, time, urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

HOME = Path(os.environ.get("ACTION_LEDGER_HOME") or Path.home() / ".agent-runs" / "action-ledger")
RUNS, PORT_FILE, PID_FILE, INDEX = HOME / "runs", HOME / "port", HOME / "pid", HOME / "index.html"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "ask-index.html"
FIRST_PORT, PORT_TRIES, VERSION = 47391, 20, 4
NAME = f"action-ledger/{VERSION}"


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def ticket_yaml(path):
    try:
        with path.open(encoding="utf-8") as file:
            head = file.read(2000).split("---", 2)
    except OSError:
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
    except OSError:
        return []


def run_view(key, data):
    run = dict(data.get("run") or {}) if isinstance(data, dict) else {}
    base, asks, updated = Path(run.get("dir") or "/nonexistent"), [], 0
    if not base.is_dir():
        return None
    for path in sorted((base / "tickets").glob("*.md")):
        try:
            updated = max(updated, path.stat().st_mtime)
        except OSError:
            continue
        meta = ticket_yaml(path)
        if meta.get("presentation") not in ("presented", "upcoming") or meta.get("status") in ("resolved", "cancelled"):
            continue
        try:
            page = (base / "asks" / f"{path.stem}.html").read_text(encoding="utf-8")
        except OSError:
            page = ""
        asks.append({"id": path.stem, "type": meta.get("type"), "presentation": meta["presentation"],
                     "action": page_value(page, "summary") or meta.get("title"),
                     "reason": page_value(page, "why"), "presentedAt": page_value(page, "presentedAt")})
    if updated:
        run["updatedAt"] = datetime.fromtimestamp(updated).astimezone().isoformat()
    statuses = goal_statuses(base)
    run["looksComplete"] = bool(statuses) and not asks and set(statuses) <= {"achieved", "abandoned"}
    return {"key": key, "run": run, "asks": asks}


class Handler(BaseHTTPRequestHandler):
    server_version = NAME

    def local(self):
        return self.headers.get("Host", "").rsplit(":", 1)[0] in ("127.0.0.1", "localhost")

    def do_POST(self):
        parts = unquote(urlsplit(self.path).path).split("/")
        if not self.local() or self.headers.get("X-Action-Ledger") != "complete" or len(parts) != 4 or parts[1::2] != ["r", "complete"]:
            return self.send_error(403)
        path = RUNS / f"{parts[2]}.json"
        view = run_view(parts[2], read_json(path))
        if not (view and view["run"]["looksComplete"]):
            return self.send_error(409, "Run does not look complete")
        path.unlink(missing_ok=True)
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


def start():
    RUNS.mkdir(parents=True, exist_ok=True)
    if page_version(TEMPLATE) > page_version(INDEX):
        shutil.copyfile(TEMPLATE, INDEX)
    running = running_version()
    if running is not None and running < VERSION:
        try:
            os.kill(int(PID_FILE.read_text()), signal.SIGTERM)
        except (OSError, ValueError):
            pass
        running = None if wait_for(lambda: running_version() is None) else running
    if running is None:
        flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        subprocess.Popen([sys.executable, __file__, "serve"], start_new_session=True, creationflags=flags,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not wait_for(lambda: running_version() is not None):
            sys.exit(f"{NAME}: server did not start")
    print(f"http://127.0.0.1:{saved_port()}/")


def run_file(run_dir):
    run_dir = Path(run_dir).resolve()
    project = next((p.parent.name for p in run_dir.parents if p.name == ".agent-runs"), run_dir.parent.name)
    return run_dir, project, RUNS / f"{project}--{run_dir.name}.json"


def register(run_dir, name=None):
    run_dir, project, path = run_file(run_dir)
    RUNS.mkdir(parents=True, exist_ok=True)
    run = {"id": run_dir.name, "name": run_dir.name, "project": project, **((read_json(path) or {}).get("run") or {})}
    path.write_text(json.dumps({"run": {**run, **({"name": name} if name else {}), "dir": str(run_dir)}}), encoding="utf-8")
    start()


def complete(run_dir):
    run_file(run_dir)[2].unlink(missing_ok=True)


if __name__ == "__main__":
    command, *args = sys.argv[1:] or ["start"]
    {"start": start, "serve": serve, "register": register, "complete": complete}[command](*args)
