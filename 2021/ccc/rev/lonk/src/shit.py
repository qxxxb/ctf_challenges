class Node:
    """Node in a linked list"""
    def __init__(self, next=None):
        self.next = next

    def __str__(self):
        """Visualize the linked list"""
        c = self
        ans = "["
        while c:
            ans += "."
            c = c.next
        return ans + "]"

    def __repr__(self):
        return str(self)


def from_int(a):
    """Convert an int to a linked list with that length"""
    h = Node()
    c = h
    while a > 0:
        c.next = Node()
        c = c.next
        a -= 1
    return h.next


def to_int(a):
    """Length of linked list"""
    i = 0
    while a:
        i += 1
        a = a.next
    return i


def copy(a):
    """Make a copy of a linked list"""
    h = Node()
    b = h
    while a:
        b.next = Node()
        b = b.next
        a = a.next
    return h.next


def add(a, b):
    """a + b"""

    h = copy(a)

    # Walk to tail of `a`
    c = h
    while c.next:
        c = c.next

    # Connect tail to a copy of `b`
    c.next = copy(b)

    # Return head
    return h


def sub(a, b):
    """a - b"""
    h = copy(a)
    c = h
    d = b
    while d:
        c = c.next
        d = d.next
    return c


def mul(a, b):
    """a * b"""
    h = Node()
    c = a
    while c:
        h = add(h, b)
        c = c.next
    return h.next


def mod(a, b):
    """a % b"""
    r = copy(b)
    c = r
    while c.next:
        c = c.next
    c.next = r

    d = r
    c = a
    while c.next:
        d = d.next
        c = c.next

    # Shitty hack
    if id(d.next) == id(r):
        r = None
    else:
        d.next = None

    return r


def power(a, b):
    """a ** b"""
    h = Node()
    c = b
    while c:
        h = mul(h, a)
        c = c.next
    return h


def powermod(a, b, m):
    """pow(a, b, m) == (a ** b) % m"""
    return mod(power(a, b), m)


def pc(n):
    """Print char"""
    print(chr(to_int(n)), end="", flush=True)


if __name__ == "__main__":
    # Lazy unit-tests

    import random
    random.seed(1337)

    xs = [random.randint(0, 1000) for _ in range(100)]
    ys = [random.randint(0, 1000) for _ in range(100)]

    for i in range(len(xs)):
        x = from_int(xs[i])
        y = from_int(ys[i])
        z = add(x, y)
        assert xs[i] + ys[i] == to_int(z)

    xs = [random.randint(1000, 2000) for _ in range(100)]
    ys = [random.randint(0, 1000) for _ in range(100)]

    for i in range(len(xs)):
        x = from_int(xs[i])
        y = from_int(ys[i])
        z = sub(x, y)
        assert xs[i] - ys[i] == to_int(z)

    xs = [random.randint(0, 10) for _ in range(100)]
    ys = [random.randint(0, 100) for _ in range(100)]

    for i in range(len(xs)):
        x = from_int(xs[i])
        y = from_int(ys[i])
        z = mul(x, y)
        assert xs[i] * ys[i] == to_int(z)

    xs = [random.randint(0, 1000) for _ in range(100)]
    ys = [random.randint(1, 1000) for _ in range(100)]

    for i in range(len(xs)):
        x = from_int(xs[i])
        y = from_int(ys[i])
        z = mod(x, y)
        assert xs[i] % ys[i] == to_int(z)

    xs = [random.randint(0, 5) for _ in range(10)]
    ys = [random.randint(0, 4) for _ in range(10)]

    for i in range(len(xs)):
        x = from_int(xs[i])
        y = from_int(ys[i])
        z = power(x, y)
        assert xs[i] ** ys[i] == to_int(z)
