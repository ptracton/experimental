
#include "syscalls.h"

void _exit(int __status) {
    UNUSED(__status);
    while(1);
}

extern int main(void);

void _start(void ) {
    main();
    return;    
}
