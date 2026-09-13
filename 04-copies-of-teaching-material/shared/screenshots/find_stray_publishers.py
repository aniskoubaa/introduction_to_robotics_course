#!/usr/bin/env python3
"""Name every `ros2 topic pub` that is actually running, and nothing else.

`pgrep -f 'ros2 topic pub'` matches the shell that is running the search,
because that string is in its own command line. That is not a nuisance: acted
on, it kills the caller. This walks /proc instead, skips this process's own
ancestry, and requires the real argument shape -- a python interpreter running
the ros2 CLI with `topic pub` as adjacent arguments.

Prints one `pid  command` line per stray and exits 1 if there were any.
"""
import os
import sys


def argv_of(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return [a for a in f.read().decode(errors="replace").split("\0") if a]
    except OSError:
        return []


def parent_of(pid):
    try:
        with open(f"/proc/{pid}/stat") as f:
            return int(f.read().rsplit(")", 1)[1].split()[1])
    except (OSError, IndexError, ValueError):
        return 0


def main():
    mine, pid = set(), os.getpid()
    while pid > 1:
        mine.add(pid)
        pid = parent_of(pid)

    strays = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        pid = int(entry)
        if pid in mine:
            continue
        argv = argv_of(pid)
        if len(argv) < 4:
            continue
        # argv[0] is the interpreter, argv[1] ends in /ros2, then "topic pub"
        if "python" not in os.path.basename(argv[0]):
            continue
        if not argv[1].endswith("/ros2") and os.path.basename(argv[1]) != "ros2":
            continue
        if argv[2:4] != ["topic", "pub"]:
            continue
        strays.append((pid, " ".join(argv[1:])))

    for pid, cmd in strays:
        print(f"{pid}  {cmd}")
    return 1 if strays else 0


if __name__ == "__main__":
    sys.exit(main())
