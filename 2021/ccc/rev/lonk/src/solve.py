def from_int(a):
    return a


def to_int(a):
    return a


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def mod(a, b):
    return a % b


def power(a, b):
    return a ** b


def powermod(a, b, m):
    return pow(a, b, m)


def pc(n):
    print(chr(to_int(n)), end="", flush=True)
