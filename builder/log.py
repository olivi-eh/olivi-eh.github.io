import os
import sys
import time
from contextlib import contextmanager

USE_COLOR = 'NO_COLOR' not in os.environ and ('FORCE_COLOR' in os.environ or sys.stdout.isatty())


class BuildError(Exception):
    """An expected build failure, reported without a traceback."""


def _style(code):
    def apply(text):
        return f'\033[{code}m{text}\033[0m' if USE_COLOR else str(text)
    return apply


bold = _style('1')
dim = _style('2')
red = _style('31')
green = _style('32')
yellow = _style('33')
cyan = _style('36')


def format_duration(seconds):
    return f'{seconds * 1000:.0f} ms' if seconds < 1 else f'{seconds:.1f} s'


def timestamp():
    return dim(time.strftime('%H:%M:%S'))


def error(message):
    lines = str(message).splitlines() or ['']
    print(f'{red("✗")} {bold(red(lines[0]))}', flush=True)
    for line in lines[1:]:
        print(f'    {line.strip()}', flush=True)


class Step:
    def __init__(self):
        self.detail = ''


class BuildLog:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.warnings = []
        self.start = time.perf_counter()

    def warn(self, message):
        self.warnings.append(message)
        print(f'  {yellow("!")} {message}', flush=True)

    @contextmanager
    def step(self, label):
        step = Step()
        start = time.perf_counter()
        try:
            yield step
        except Exception:
            if self.verbose:
                print(f'  {red("✗")} {label}', flush=True)
            raise
        if self.verbose:
            elapsed = format_duration(time.perf_counter() - start)
            print(f'  {green("✓")} {label:<16} {dim(f"{step.detail:<34}")} {dim(f"{elapsed:>7}")}', flush=True)

    def done(self, summary):
        elapsed = format_duration(time.perf_counter() - self.start)
        warnings = f' {yellow(f"with {len(self.warnings)} warning(s)")}' if self.warnings else ''
        print(f'{green("✓")} {bold(summary)} {dim(f"in {elapsed}")}{warnings}', flush=True)
