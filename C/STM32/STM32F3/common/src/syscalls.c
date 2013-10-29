
#ifndef UNUSED
#define UNUSED(x) (void)x
#endif


void _exit(int __status) {
    UNUSED(__status);
    while(1);
}

extern int main(void);

void _start(void ) {
    main();
    return;    
}
