#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // This sometimes works, sometimes doesn't. Depends on the server load

    unsigned char* buf = (unsigned char*)argv[1];

    char ans[4] = "ABCD";

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 256; ++j) {
            if (j == ans[i] && buf[i] == ans[i]) {
                ans[i] = 0;
            }
        }
    }

    if (!ans[0] && !ans[1] && !ans[2] && !ans[3]) {
        return 0;
    } else {
        return 1;
    }
}
