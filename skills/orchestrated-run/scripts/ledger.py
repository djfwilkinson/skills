#!/usr/bin/env python3
"""Device-level action ledger for orchestrated runs. Python 3.9+, stdlib only.

  python3 ledger.py        create the ledger if missing, replace its index when
                           the template's ledger-version is newer, start the
                           server if it is not running, and print the index URL
  python3 ledger.py serve  run the server in the foreground

Each run writes runs/<key>.json under the ledger directory and deletes it on
completion. The server serves the index, merges runs/*.json at /runs, and
serves files under each run's directory at /r/<key>/<path>.
"""
import json, mimetypes, os, re, shutil, socket, subprocess, sys, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

HOME = Path(os.environ.get("ACTION_LEDGER_HOME") or Path.home() / ".agent-runs" / "action-ledger")
RUNS, PORT_FILE, INDEX = HOME / "runs", HOME / "port", HOME / "index.html"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "ask-index.html"
FIRST_PORT, PORT_TRIES, NAME = 47391, 20, "action-ledger/1"


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def runs():
    found = []
    for path in sorted(RUNS.glob("*.json")):
        data = read_json(path)
        if isinstance(data, dict):
            found.append({**data, "key": path.stem})
    return found


class Handler(BaseHTTPRequestHandler):
    server_version = NAME

    def do_GET(self):
        if self.headers.get("Host", "").rsplit(":", 1)[0] not in ("127.0.0.1", "localhost"):
            return self.send_error(403)
        path = unquote(urlsplit(self.path).path)
        if path == "/":
            return self.send(INDEX.read_bytes(), "text/html")
        if path == "/runs":
            return self.send(json.dumps(runs()).encode(), "application/json")
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


def is_ledger(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/runs", timeout=1) as reply:
            return reply.headers.get("Server", "").startswith(NAME)
    except Exception:
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
    if not is_ledger(saved_port()):
        flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        subprocess.Popen([sys.executable, __file__, "serve"], start_new_session=True, creationflags=flags,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            time.sleep(0.1)
            if is_ledger(saved_port()):
                break
        else:
            sys.exit(f"{NAME}: server did not start")
    print(f"http://127.0.0.1:{saved_port()}/")


if __name__ == "__main__":
    serve() if sys.argv[1:] == ["serve"] else start()
