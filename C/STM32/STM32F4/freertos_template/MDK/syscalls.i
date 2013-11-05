#line 1 "..\\..\\common\\src\\syscalls.c"

#line 1 "..\\..\\common\\includes\\syscalls.h"








#line 3 "..\\..\\common\\src\\syscalls.c"

void _exit(int __status) {
    (void)__status;
    while(1);
}

extern int main(void);

void _start(void ) {
    main();
    return;    
}
