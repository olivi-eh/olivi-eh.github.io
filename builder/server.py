import http.server
import sys
import threading
import time
from pathlib import Path

from builder.config import (
    NOTES_DIR,
    OUT_DIR,
    ROOT_DIR,
    STATIC_DIR,
    STATIC_ROOT_DIR,
    TEMPLATES_DIR,
)
from builder.log import BuildError, bold, cyan, dim, error, timestamp
from builder.renderer import build

PORT = 8082
WATCH_DIRS = [NOTES_DIR, TEMPLATES_DIR, STATIC_DIR, STATIC_ROOT_DIR]


def snapshot():
    files = {}
    for directory in WATCH_DIRS:
        for p in directory.rglob('*'):
            # Skip hidden files (.DS_Store, editor swap files) and backups
            if any(part.startswith('.') for part in p.relative_to(directory).parts) or p.name.endswith('~'):
                continue
            try:
                if p.is_file():
                    files[p] = p.stat().st_mtime
            except OSError:
                pass
    return files


def describe_changes(before, after):
    changed = sorted(
        p.relative_to(ROOT_DIR).as_posix()
        for p in before.keys() | after.keys()
        if before.get(p) != after.get(p)
    )
    if len(changed) == 1:
        return changed[0]
    return f'{changed[0]} {dim(f"and {len(changed) - 1} more")}'


def describe_exception(e):
    location = ''
    if getattr(e, 'filename', None) and getattr(e, 'lineno', None):
        location = f' ({Path(e.filename).resolve().relative_to(ROOT_DIR, walk_up=True)}:{e.lineno})'
    return f'{type(e).__name__}: {e}{location}'


def safe_build(verbose):
    try:
        build(dev=True, verbose=verbose)
    except BuildError as e:
        error(e)
    except Exception as e:
        error(describe_exception(e))


def create_server(directory, port):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, format, *args):
            # Suppress normal server logs to keep rebuild console clean
            pass

    return http.server.ThreadingHTTPServer(('', port), Handler)


def watch_and_serve():
    safe_build(verbose=True)

    try:
        server = create_server(OUT_DIR, PORT)
    except OSError as e:
        error(f'Could not start server on port {PORT}: {e.strerror}\nIs another dev server already running?')
        sys.exit(1)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    watched = ' '.join(f'{d.name}/' for d in WATCH_DIRS)
    print()
    print(f'  {cyan("➜")} {bold("Local:")}     {cyan(f"http://localhost:{PORT}/")}', flush=True)
    print(f'  {dim("➜")} {dim("Watching:")}  {dim(watched)}', flush=True)
    print(f'  {dim("➜")} {dim("Press Ctrl+C to stop")}', flush=True)
    print()

    files = snapshot()
    try:
        while True:
            time.sleep(0.5)
            current = snapshot()
            if current != files:
                print(f'{timestamp()} {describe_changes(files, current)}', flush=True)
                safe_build(verbose=False)
                files = current
    except KeyboardInterrupt:
        print(f'\n{dim("Stopped dev server.")}', flush=True)
