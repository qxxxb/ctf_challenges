#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // import pwn
    // enc = bytes.fromhex("20a431f8")
    // key = pwn.xor(enc, b"ABCD")

    char enc[4] = {0x20, 0xa4, 0x31, 0xf8};
    unsigned char* input = (unsigned char*)argv[1];

    for (int i = 0; i < 4; ++i) {
        input[i] ^= enc[i];
    }

    if (input[0] == 0x61 &&
        input[1] == 0xe6 &&
        input[2] == 0x72 &&
        input[3] == 0xbc
    ) {
        return 0;
    } else {
        return 1;
    }
}
