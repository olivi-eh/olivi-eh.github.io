import http.server
import threading
import time

from builder.config import (
    NOTES_DIR,
    OUT_DIR,
    STATIC_DIR,
    STATIC_ROOT_DIR,
    TEMPLATES_DIR,
)
from builder.renderer import build


def get_max_mtime():
    paths_to_watch = [NOTES_DIR, TEMPLATES_DIR, STATIC_DIR, STATIC_ROOT_DIR]
    max_mtime = 0.0
    for path in paths_to_watch:
        if not path.exists():
            continue
        for p in path.rglob('*'):
            try:
                mtime = p.stat().st_mtime
                if mtime > max_mtime:
                    max_mtime = mtime
            except OSError:
                pass

    return max_mtime


def serve_directory(directory=OUT_DIR, port=8082):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, format, *args):
            # Suppress normal server logs to keep rebuild console clean
            pass

    server = http.server.ThreadingHTTPServer(('', port), Handler)
    server.socket.setsockopt(http.server.socket.SOL_SOCKET, http.server.socket.SO_REUSEADDR, 1)

    print(f"🚀 Local development server running at: http://localhost:{port}/", flush=True)
    try:
        server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}", flush=True)


def watch_and_serve():
    # Initial build before serving
    print("🛠️ Building...", flush=True)
    build()

    # Start the HTTP server in a daemon thread
    server_thread = threading.Thread(target=serve_directory, args=(OUT_DIR, 8082), daemon=True)
    server_thread.start()

    print("👀 Watching for changes in notes/, templates/, and static/...", flush=True)
    last_mtime = get_max_mtime()
    try:
        while True:
            time.sleep(1.0)
            current_mtime = get_max_mtime()
            if current_mtime > last_mtime:
                print("\n🛠️ Change detected! Rebuilding...", flush=True)
                try:
                    build()
                except Exception as e:
                    print(f"❌ Rebuild failed: {e}", flush=True)
                last_mtime = current_mtime
    except KeyboardInterrupt:
        print("\nStopping watch and server. Bye!", flush=True)
