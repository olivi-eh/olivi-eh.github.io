import sys
from builder import build, watch_and_serve
from builder.log import BuildError, error


def main():
    if '--serve' in sys.argv or '--watch' in sys.argv:
        watch_and_serve()
    else:
        try:
            build()
        except BuildError as e:
            error(e)
            sys.exit(1)


if __name__ == '__main__':
    main()
