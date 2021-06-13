# angrbox

Write me a program that:
- Takes 4 uppercase characters in argv
- Verifies the 4 character key and returns 0 if correct
- If I find the key, YOU LOSE

```
nc 35.194.4.79 7000
```

Attachments: `angrbox.zip`

## Solution

The server tries to solve user-supplied binaries with angr. To get the flag,
users have to write "obfuscated" binaries that angr won't be able to easily
solve.

An easy way to do this is [path explosion](https://youtu.be/VJoNraxFliM), which
will cause angr to use an exponential amount of memory.

Here's my solution `solve.c`:

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    char* buf = argv[1];
    char ans[4] = {0};

    // Path explosion (26**4)
    for (int i = 0; i < 4; ++i) {
        if (buf[i] == 'A') ans[i] = 0;
        else if (buf[i] == 'B') ans[i] = 1;
        else if (buf[i] == 'C') ans[i] = 2;
        else if (buf[i] == 'D') ans[i] = 3;
        // ...
        else if (buf[i] == 'X') ans[i] = 23;
        else if (buf[i] == 'Y') ans[i] = 24;
        else if (buf[i] == 'Z') ans[i] = 25;
    }

    if (ans[0] == 0 &&
        ans[1] == 1 &&
        ans[2] == 2 &&
        ans[3] == 3
    ) {
        return 0;
    } else {
        return 1;
    }
}
```

Output:

```
$ python3 solve.py
[+] Opening connection to 35.194.4.79 on port 7000: Done
[*] Solving PoW: sha256(????03g5mD9PIYCC) == 71f22b28a9c0d0d2a7d9451f40c7932d4ebe45ee467dccae3816e8c073e9280a
[+] prefix = stYi
[*] Queued in position 0
[+] Handling your job now
[*] Switching to interactive mode
[*] Compiling ...
[*] Solving (max 2 minutes) ...
WARNING | 2021-06-13 17:31:10,410 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
[*] My solver couldn't find a key >:(
[*] Gimme ur key and I'll check it: $ ABCD
[*] WTF? YOUR KEY WORKS
[*] You are a crypto genius
[+] Here's your flag: CCC{p4th_3pl0s10n_4s_a_tr4pd00r_funct10n?_0r_d1d_y0u_ch33s3_1t}
[*] Got EOF while reading in interactive
```

## Bonus

An interesting unintended solution from Reelix:

```c
int main(int argc, char** argv) {
   char* s = argv[1];
   char c = 'Z';
   strncat(s, &c, 1);
   char correct[] = "ABCDZ";
   return strcmp(s, correct) != 0;
}
```

Somehow `strncat` confuses angr (maybe null-byte issues?) causing it to reach
one dead-ended state but no key.

Output:

```
$ python3 solve.py reelix.c
[+] Opening connection to 35.194.4.79 on port 7000: Done
[*] Solving PoW: sha256(????4sCYAWfEWbVD) == 8ef56145b5f0f55d91ca167cf92cf2b6f52b10b6e4edcd982ae9778cf84b00d3
[+] prefix = 0IUJ
[*] Queued in position 0
[+] Handling your job now
[*] Switching to interactive mode
[*] Compiling ...
/opt/transfer/4219cc56.c: In function 'main':
/opt/transfer/4219cc56.c:4:4: warning: implicit declaration of function 'strncat' [-Wimplicit-function-declaration]
    strncat(s, &c, 1);
    ^~~~~~~
/opt/transfer/4219cc56.c:4:4: warning: incompatible implicit declaration of built-in function 'strncat'
/opt/transfer/4219cc56.c:4:4: note: include '<string.h>' or provide a declaration of 'strncat'
/opt/transfer/4219cc56.c:6:11: warning: implicit declaration of function 'strcmp' [-Wimplicit-function-declaration]
    return strcmp(s, correct) != 0;
           ^~~~~~
[*] Solving (max 2 minutes) ...
WARNING | 2021-06-13 17:37:22,047 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
WARNING | 2021-06-13 17:37:23,967 | angr.storage.memory_mixins.default_filler_mixin | The program is accessing memory or registers with an unspecified value. This could indicate unwanted behavior.
WARNING | 2021-06-13 17:37:23,967 | angr.storage.memory_mixins.default_filler_mixin | angr will cope with this by generating an unconstrained symbolic variable and continuing. You can resolve this by:
WARNING | 2021-06-13 17:37:23,967 | angr.storage.memory_mixins.default_filler_mixin | 1) setting a value to the initial state
WARNING | 2021-06-13 17:37:23,967 | angr.storage.memory_mixins.default_filler_mixin | 2) adding the state option ZERO_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to make unknown regions hold null
WARNING | 2021-06-13 17:37:23,967 | angr.storage.memory_mixins.default_filler_mixin | 3) adding the state option SYMBOL_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to suppress these messages.
WARNING | 2021-06-13 17:37:23,967 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0x7ffffffffff0000 with 88 unconstrained bytes referenced from 0x700010 (strncat+0x0 in extern-address space (0x10))
WARNING | 2021-06-13 17:37:24,058 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0x7fffffffffeff60 with 8 unconstrained bytes referenced from 0x700010 (strncat+0x0 in extern-address space (0x10))
[*] Got 1 dead-ended states
[*] My solver couldn't find a key >:(
[*] Gimme ur key and I'll check it: $ ABCD
[*] WTF? YOUR KEY WORKS
[*] You are a crypto genius
[+] Here's your flag: CCC{p4th_3pl0s10n_4s_a_tr4pd00r_funct10n?_0r_d1d_y0u_ch33s3_1t}
[*] Got EOF while reading in interactive
```
