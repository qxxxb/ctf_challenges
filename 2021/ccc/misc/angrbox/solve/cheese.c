#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    char *buf = argv[1];
    // Returns 0x2a00 for some reason
    int x = system("exit 42");

    if ((buf[0] ^ x) == 0x2a41 &&
        (buf[1] ^ x) == 0x2a42 &&
        (buf[2] ^ x) == 0x2a43 &&
        (buf[3] ^ x) == 0x2a44
    ) {
        return 0;
    } else {
        return 1;
    }
}
