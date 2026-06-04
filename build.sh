mkdir -p sysroot/{bin,sbin,etc,lib,dev,proc,sys}
gcc -static src/bin/utility.c -o sysroot/bin/utility