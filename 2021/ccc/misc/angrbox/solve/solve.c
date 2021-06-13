#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    char* buf = argv[1];
    char ans[4] = {0};

    // Path explosion (26**4)
    // https://youtu.be/VJoNraxFliM

    for (int i = 0; i < 4; ++i) {
        if (buf[i] == 'A') ans[i] = 0;
        else if (buf[i] == 'B') ans[i] = 1;
        else if (buf[i] == 'C') ans[i] = 2;
        else if (buf[i] == 'D') ans[i] = 3;
        else if (buf[i] == 'E') ans[i] = 4;
        else if (buf[i] == 'F') ans[i] = 5;
        else if (buf[i] == 'G') ans[i] = 6;
        else if (buf[i] == 'H') ans[i] = 7;
        else if (buf[i] == 'I') ans[i] = 8;
        else if (buf[i] == 'J') ans[i] = 9;
        else if (buf[i] == 'K') ans[i] = 10;
        else if (buf[i] == 'L') ans[i] = 11;
        else if (buf[i] == 'M') ans[i] = 12;
        else if (buf[i] == 'N') ans[i] = 13;
        else if (buf[i] == 'O') ans[i] = 14;
        else if (buf[i] == 'P') ans[i] = 15;
        else if (buf[i] == 'Q') ans[i] = 16;
        else if (buf[i] == 'R') ans[i] = 17;
        else if (buf[i] == 'S') ans[i] = 18;
        else if (buf[i] == 'T') ans[i] = 19;
        else if (buf[i] == 'U') ans[i] = 20;
        else if (buf[i] == 'V') ans[i] = 21;
        else if (buf[i] == 'W') ans[i] = 22;
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
