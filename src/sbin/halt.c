#include <unistd.h>
#include <sys/reboot.h>
#include <stdio.h>

int main() {
    printf("Syncing filesystem...");

    sync();

    printf(" Done!\n");

    printf("Halting system...");
    if (reboot(RB_HALT_SYSTEM) == -1) {
        perror("Failed to halt system");
        return 1;
    }

    return 0;
}