# lonk

I found a script that prints the flag! Unfortunately it's a bit slow...

Attachments:
- `flag.py`
- `lib.py`

## TLDR

`lib.py` implements simple arithmetic operations on numbers represented on
linked lists. However, this means large numbers take a huge amount of memory,
which makes it impossible to print the flag from `flag.py` using the current
implementation.

Solution: Reverse each function and replace it with a usual implementation on
integers.

```
%s/我/Node/g
%s/非/from_int/g
%s/常/to_int/g
%s/需/copy/g
%s/要/add/g
%s/放/sub/g
%s/屁/mul/g
%s/然/mod/g
%s/後/power/g
%s/睡/pow/g
%s/覺/print_char/g
```

## Solution

Running `flag.py` gives
```
$ python3 flag.py
CCC{m4Th
```

It takes about 3 seconds for it to print `T` and 50 seconds to print `h` on my laptop.

Looking at the code, `flag.py` seems to be filled with nonsense:
```python
from lib import *

覺(非(67))
覺(要(非(34), 非(33)))
覺(要(放(非(105), 非(58)), 非(20)))
覺(屁(非(3), 非(41)))
覺(然(非(811), 非(234)))
覺(睡(非(3), 非(5), 非(191)))

# ...
```

The actual logic seems to be in `lib.py`. We can see this function

```python
def 覺(n):
    print(chr(常(n)), end="", flush=True)
```

prints out a single character, and every line of code in `flag.py` calls this
function once.

Starting from the top, the first line of code in `flag.py` is:
```python
print_char(非(67))
```

Here's the relevant function in `lib.py`
```python
class 我:
    def __init__(self, n=None):
        self.n = n

def 非(a):
    h = 我()
    c = h
    while a > 0:
        c.n = 我()
        c = c.n
        a -= 1
    return h.n
```

The class `我` looks like a linked list Node without the usual `self.data`
attribute. Knowing this, we can see that `非()` create a linked list of length
`a`.

So this linked list gets passed to the `print_char()` function, which then
calls `print(chr(常(n)), end="", flush=True)`. Here's the source for the `常()`
function:
```python
def 常(a):
    i = 0
    while a:
        i += 1
        a = a.n
    return i
```

We can see that it just calculates the length of the of the linked list.

In summary, `覺(非(67))` translates to `print_char(make_list(67))`, which
prints `C`, whose ASCII code is 67.

---

The next line of code in `flag.py` is
```python
覺(要(非(34), 非(33)))
```

Here's the code for `要()`
```python
def 要(a, b):
    h = 需(a)
    c = h
    while c.n:
        c = c.n
    c.n = 需(b)
    return h
```

First it calls `需()`
```python
def 需(a):
    h = Node()
    b = h
    while a:
        b.n = Node()
        b = b.n
        a = a.n
    return h.n
```

We can see that it just makes a copy of a linked list. Going back to `要()`, we
can see that it returns a new list whose length is the sum of the lengths of
its parameters.

```python
def 要(a, b):
    h = copy(a)

    # Walk to tail of `a`
    c = h
    while c.next:
        c = c.next

    # Connect tail to a copy of `b`
    c.next = copy(b)

    # Return head
    return h
```

So the line `覺(要(非(34), 非(33)))` prints ASCII code `34 + 33`, which ends up
being `C` again.

---

Working in a similar manner, we can see that `放(a, b)` computes `a - b`, so
`覺(要(放(非(105), 非(58)), 非(20)))` prints `105 - 58 + 20` which
prints `C`.

The next function is `屁()`.
```python
def 屁(a, b):
    h = Node()
    c = a
    while c:
        h = add(h, b)
        c = c.next
    return h.next
```

This computes `a * b`, so `覺(屁(非(3), 非(41)))` prints `3 * 41`, which is
`{`.

The next function `然()` is more interesting, and I have annotated it below:
```python
def mod(a, b):
    b_copy = copy(b)

    # Walk to the end of b's copy
    c = b_copy
    while c.next:
        c = c.next

    # Connect b_copy's tail to its head, making it a ring.
    c.next = b_copy

    # Iterate `a` using `c`, but also increment `b_copy_c` around its ring.
    b_copy_c = b_copy
    c = a
    while c.next:
        b_copy_c = b_copy_c.next
        c = c.next

    # Cut the ring where `b_copy_c` is currently at and return the starting
    # point of the ring.
    if id(b_copy_c.next) == id(b_copy):
        # Special case when we end up at the start again
        b_copy = None
    else:
        b_copy_c.next = None

    return b_copy
```

The implementation is pretty confusing, but it actually just computes `a % b`
(if you visualize modular arithmetic using clocks, it might make more sense).

Knowing this, `覺(然(非(811), 非(234)))` prints `811 % 234` which is `m`.

The last two functions left these:
```python
def 後(a, b):
    h = Node()
    c = b
    while c:
        h = mul(h, a)
        c = c.n
    return h


def 睡(a, b, m):
    return mod(後(a, b), m)
```

We can see that `後` computes `a ** b` and `睡` computes `(a ** b) % m`.
However that's not an efficient way to compute modular powers. Instead we
should use Python's built-in `pow` function `pow(a, b, m)`.

---

Now we can just replace the functions in `lib.py` with the simpler functions
we've derived, and running `flag.py` will print the flag.

```python
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

pc(from_int(67))
pc(add(from_int(34), from_int(33)))
pc(add(sub(from_int(105), from_int(58)), from_int(20)))
pc(mul(from_int(3), from_int(41)))
pc(mod(from_int(811), from_int(234)))
pc(powermod(from_int(3), from_int(5), from_int(191)))

pc(
    sub(
        mod(
            mul(
                mul(
                    mul(
                        mul(
                            mul(
                                mul(
                                    mul(
                                        mul(
                                            mul(
                                                mul(
                                                    mul(from_int(2), from_int(2)),
                                                    from_int(2),
                                                ),
                                                from_int(2),
                                            ),
                                            from_int(2),
                                        ),
                                        from_int(2),
                                    ),
                                    from_int(2),
                                ),
                                from_int(2),
                            ),
                            from_int(2),
                        ),
                        from_int(2),
                    ),
                    from_int(2),
                ),
                from_int(2),
            ),
            from_int(1337),
        ),
        from_int(1),
    )
)

pc(
    mul(
        sub(
            mul(mod(power(from_int(3), from_int(9)), from_int(555)), from_int(2)),
            from_int(464),
        ),
        from_int(2),
    )
)

pc(powermod(from_int(2020), from_int(451813409), from_int(2350755551)))

pc(
    powermod(
        from_int(1234567890),
        from_int(9431297343284265593),
        add(from_int(119), from_int(17017780892086357584)),
    )
)

pc(
    mul(
        powermod(from_int(3), sub(from_int(60437), from_int(1024)), from_int(151553)),
        powermod(
            from_int(3),
            add(
                mul(
                    from_int(5),
                    mod(
                        mul(
                            mul(
                                mul(mul(from_int(10), from_int(10)), from_int(10)),
                                from_int(10),
                            ),
                            from_int(10),
                        ),
                        from_int(1337),
                    ),
                ),
                from_int(54103),
            ),
            from_int(151553),
        ),
    )
)

pc(
    add(
        powermod(
            from_int(111111111111111111111111111111111111),
            from_int(222222222222222222222222222222222222),
            from_int(333333333333333333333333333333333333),
        ),
        mul(mul(from_int(2), from_int(2)), from_int(29)),
    )
)

pc(
    mul(
        sub(
            power(
                mul(add(from_int(1), from_int(1)), add(from_int(1), from_int(1))),
                from_int(2),
            ),
            from_int(8),
        ),
        powermod(from_int(2), from_int(7262490), from_int(98444699)),
    )
)

pc(
    sub(
        mul(mul(mul(from_int(1337), from_int(1337)), from_int(1337)), from_int(1337)),
        from_int(3195402929666),
    )
)

pc(
    sub(
        mod(
            sub(
                from_int(
                    1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
                ),
                from_int(1),
            ),
            from_int(100),
        ),
        from_int(23),
    )
)

pc(
    sub(
        mod(sub(power(from_int(100), from_int(100)), from_int(1)), from_int(100)),
        from_int(50),
    )
)

pc(
    mod(
        add(
            add(
                add(
                    add(
                        add(
                            add(
                                add(
                                    add(
                                        add(
                                            add(
                                                add(
                                                    add(
                                                        add(
                                                            add(
                                                                add(
                                                                    add(
                                                                        add(
                                                                            add(
                                                                                add(
                                                                                    from_int(
                                                                                        1
                                                                                    ),
                                                                                    from_int(
                                                                                        2
                                                                                    ),
                                                                                ),
                                                                                from_int(
                                                                                    3
                                                                                ),
                                                                            ),
                                                                            from_int(4),
                                                                        ),
                                                                        from_int(5),
                                                                    ),
                                                                    from_int(6),
                                                                ),
                                                                from_int(7),
                                                            ),
                                                            from_int(8),
                                                        ),
                                                        from_int(9),
                                                    ),
                                                    from_int(10),
                                                ),
                                                from_int(11),
                                            ),
                                            from_int(12),
                                        ),
                                        from_int(13),
                                    ),
                                    from_int(14),
                                ),
                                from_int(15),
                            ),
                            from_int(16),
                        ),
                        from_int(17),
                    ),
                    from_int(18),
                ),
                from_int(19),
            ),
            from_int(20),
        ),
        from_int(132),
    )
)

pc(
    add(
        sub(
            powermod(from_int(1337), from_int(1337), add(from_int(1337), from_int(1337))),
            from_int(1336),
        ),
        from_int(106),
    )
)

pc(add(from_int(50), from_int(1)))

pc(
    add(
        mod(
            sub(
                power(
                    power(power(from_int(10), from_int(10)), from_int(10)), from_int(10)
                ),
                from_int(1),
            ),
            from_int(100),
        ),
        from_int(1),
    )
)

pc(
    add(
        sub(
            mod(
                sub(
                    power(from_int(55555), from_int(5)),
                    mul(
                        mul(
                            mul(
                                mul(
                                    mul(
                                        mul(
                                            mul(
                                                mul(
                                                    mul(
                                                        mul(
                                                            mul(
                                                                mul(
                                                                    mul(
                                                                        mul(
                                                                            mul(
                                                                                mul(
                                                                                    mul(
                                                                                        mul(
                                                                                            mul(
                                                                                                mul(
                                                                                                    mul(
                                                                                                        mul(
                                                                                                            from_int(
                                                                                                                1
                                                                                                            ),
                                                                                                            from_int(
                                                                                                                2
                                                                                                            ),
                                                                                                        ),
                                                                                                        from_int(
                                                                                                            3
                                                                                                        ),
                                                                                                    ),
                                                                                                    from_int(
                                                                                                        4
                                                                                                    ),
                                                                                                ),
                                                                                                from_int(
                                                                                                    5
                                                                                                ),
                                                                                            ),
                                                                                            from_int(
                                                                                                6
                                                                                            ),
                                                                                        ),
                                                                                        from_int(
                                                                                            7
                                                                                        ),
                                                                                    ),
                                                                                    from_int(
                                                                                        8
                                                                                    ),
                                                                                ),
                                                                                from_int(
                                                                                    9
                                                                                ),
                                                                            ),
                                                                            from_int(
                                                                                10
                                                                            ),
                                                                        ),
                                                                        from_int(11),
                                                                    ),
                                                                    from_int(12),
                                                                ),
                                                                from_int(13),
                                                            ),
                                                            from_int(14),
                                                        ),
                                                        from_int(15),
                                                    ),
                                                    from_int(16),
                                                ),
                                                from_int(17),
                                            ),
                                            from_int(18),
                                        ),
                                        from_int(19),
                                    ),
                                    from_int(20),
                                ),
                                from_int(21),
                            ),
                            from_int(22),
                        ),
                        from_int(23),
                    ),
                ),
                from_int(1337),
            ),
            from_int(200),
        ),
        from_int(45),
    )
)

pc(powermod(from_int(6), from_int(11333), from_int(29959)))

pc(
    sub(
        mul(
            mul(
                mul(
                    mul(
                        from_int(4),
                        from_int(4),
                    ),
                    from_int(4),
                ),
                from_int(4),
            ),
            from_int(4),
        ),
        from_int(975),
    )
)

pc(
    mul(
        sub(
            add(sub(add(from_int(3), from_int(3)), from_int(1)), from_int(4)),
            from_int(3),
        ),
        sub(
            add(sub(add(from_int(3), from_int(3)), from_int(1)), from_int(4)),
            from_int(3),
        ),
    )
)

pc(
    sub(
        powermod(
            powermod(from_int(12345), from_int(12345), from_int(54321)),
            from_int(12345),
            from_int(54321),
        ),
        from_int(3037),
    )
)

pc(add(from_int(50), from_int(3)))
pc(from_int(125))

print()
```

Output:
```
CCC{m4Th_w1tH_L1Nk3d_l1$t5}
```
