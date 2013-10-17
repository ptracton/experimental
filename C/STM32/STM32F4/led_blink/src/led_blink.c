#include <libopencm3/stm32/gpio.h>
#include "system_stm32f4.h"
#include "leds.h"

int main(void)
{
    uint32_t i;
    
    SystemInit();
    
    LED_Init();
    
    while (1) {
	LED_Toggle(LED_GREEN);	
	for (i = 0; i < 2000000; i++) /* Wait a bit. */
	    __asm__("nop");	
    }

    return 0;
}
