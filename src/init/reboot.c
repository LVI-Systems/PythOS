#include <stdio.h>
#include <unistd.h>
#include <sys/reboot.h>

int main() {
    printf("Syncing filesystem... ");
    sync();
    printf("Done!\n");

    printf("Rebooting...");
    if (reboot(RB_AUTOBOOT) == -1) {
        perror("Reboot faield");
        return 1;
    }

    return 0;
}