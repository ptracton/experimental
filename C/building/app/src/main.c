
#include "stdint.h"

#include "lib1.h"
#include "lib2.h"
#include "common.h"
#include "app.h"

int main(void)
{
    FOO_Type foo;
    foo.foo = 5;
    foo.bar = foo.foo;
    
    lib1_call();
    lib2_call();
    common_call();
    return 0;    
}
