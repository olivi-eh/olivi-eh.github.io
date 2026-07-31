import sys
from builder import build, watch_and_serve


def main():
    if '--serve' in sys.argv or '--watch' in sys.argv:
        watch_and_serve()
    else:
        print("🛠️ Building...", flush=True)
        build()


if __name__ == '__main__':
    main()
