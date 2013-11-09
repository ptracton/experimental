
#include "syscalls.h"
#include "ch.h"
#include "leds.h"
#include "thread1.h"

Thread * Thread1_ptr;

WORKING_AREA(Thread1Area, 128);

msg_t Thread1(void * arg)
{
    msg_t msg;
    
    UNUSED(arg);
    
    while(TRUE){	
	chSysLock();
	Thread1_ptr = chThdSelf();
	chSchGoSleepS(THD_STATE_SUSPENDED);
	msg = chThdSelf()->p_u.rdymsg;  /* Retrieving the message, optional.*/
	chSysUnlock();
	
	LEDS_Toggle(BLUE);
    }
    
    return (msg_t) 0;
}
