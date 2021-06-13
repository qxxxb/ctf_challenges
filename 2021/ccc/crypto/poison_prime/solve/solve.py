import pwn
import Crypto.Util.number as cun
import Crypto.Random.random as crr
import Crypto.Util.Padding as cup
from Crypto.Cipher import AES
import hashlib


def subgroup_attack(ct, p, g):
    x = g
    while x != 1:
        shared_key = x
        aes_key = hashlib.sha1(cun.long_to_bytes(shared_key)).digest()[:16]
        cipher = AES.new(aes_key, AES.MODE_ECB)
        try:
            pt = cup.unpad(cipher.decrypt(ct), 16)
            if b"My favorite food is " in pt:
                return pt
        except:
            pass

        x = (x * g) % p


# io = pwn.process("python3 ../dist/server.py", shell=True)
# io = pwn.remote("localhost", 4000)
io = pwn.remote("35.224.135.84", 4000)

# Mersenne prime: https://www.mersenne.org/primes
p = (1 << 2203) - 1

# Prime factor of (p - 1) from factordb:
# http://factordb.com/index.php?query=2%5E2203+-+2
q = 711718443060888357455104383759579899185453159253854240850359788937324328008225366876777905349283339583535597500393178373807851032788989008946432082299780350922963303

io.sendlineafter("Please help them choose p: ", str(p))
io.sendlineafter("give me a large prime factor of (p - 1): ", str(q))

io.recvuntil("Here's their encrypted message: ")
ct = bytes.fromhex(io.recvlineS())

pt = subgroup_attack(ct, p, g=8)
io.sendlineafter("Decrypt it and I'll give you the flag: ", pt)
io.interactive()
