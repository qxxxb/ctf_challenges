import pwn
import sys
import hashlib
import itertools
import string

"""
cheese.c: Fails due to seccomp
forkbomb.c: Fails due to seccomp
easy0.c: Fails because angr solves it
easy1.c: Fails because angr solves it
easy2.c: Fails because angr solves it
easy3.c: Sometimes fails because angr solves it, sometimes passes
solve.c: Passes because angr will use tons of memory and exits
"""


def solve_pow(io):
    suffix = io.recvlineS().strip().split(" = ")[-1]
    h = io.recvlineS().strip().split(" = ")[-1]
    prefix_len = int(io.recvuntilS(": ").lstrip("[*] Give me the ").split()[0])
    print("[*] Solving PoW: sha256({}{}) == {}".format("?" * prefix_len, suffix, h))

    pool = string.ascii_letters + string.digits
    for p in itertools.product(pool, repeat=prefix_len):
        prefix = "".join(p)
        if hashlib.sha256((prefix + suffix).encode()).hexdigest() == h:
            print("[+] prefix = " + prefix)
            io.sendline(prefix)
            return
    else:
        print("[-] Solution not found")


# io = pwn.remote("localhost", 7000)
io = pwn.remote("35.194.4.79", 7000)
solve_pow(io)

print(io.recvlineS().strip())  # Queue position
print(io.recvlineS().strip())  # Ready notification

f = sys.argv[1] if len(sys.argv) == 2 else "solve.c"
src = open(f, "rb").read()
io.sendlineafter("hex:\n", src.hex())
io.interactive()
