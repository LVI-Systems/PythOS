#include <unistd.h>
#include <stdio.h>
#include <sys/reboot.h>

int main() {
    printf("Syncing filesystem... ");
    sync();
    printf("Done!\n");

    printf("Shutting down...\n");
    if (reboot(RB_POWER_OFF) == -1) {
        perror("Failed to shutdown");
        return 1;
    }
    return 0;
}