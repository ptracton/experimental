#include <stm32f30x.h>
#include "leds.h"

#define WAIT_1SECOND 8000000

void Wait(uint32_t time)
{
    volatile uint32_t i;
    for (i=0; i<time; i++);
    return;    
}


int main(void)
{
    LEDS_Init();
    
    while(1){
	LEDS_Toggle(LED_0);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_1);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_2);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_3);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_4);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_5);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_6);
	Wait(WAIT_1SECOND);
	LEDS_Toggle(LED_7);
	Wait(WAIT_1SECOND);	
    }
    

    return 0;    
}
