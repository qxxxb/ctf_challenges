#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // import pwn
    // a = bytes.fromhex("20a431f8")
    // b = bytes.fromhex("450eb371")
    // c = bytes.fromhex("1290c822")
    // key = pwn.xor(a, b, c, b"ABCD")

    char enc1[4] = {0x20, 0xa4, 0x31, 0xf8};
    char enc2[4] = {0x45, 0x0e, 0xb3, 0x71};
    char enc3[4] = {0x12, 0x90, 0xc8, 0x22};
    unsigned char* input = (unsigned char*)argv[1];

    for (int i = 0; i < 4; ++i) {
        input[i] ^= enc1[i];
    }

    for (int i = 0; i < 4; ++i) {
        input[i] ^= enc2[i];
    }

    for (int i = 0; i < 4; ++i) {
        input[i] ^= enc3[i];
    }

    // 367809ef
    if (input[0] == 0x36 &&
        input[1] == 0x78 &&
        input[2] == 0x09 &&
        input[3] == 0xef
    ) {
        return 0;
    } else {
        return 1;
    }
}
