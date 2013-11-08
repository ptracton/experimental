#include <stm32f4xx.h>
#include "ch.h"
#include "timer2.h"
#include "leds.h"


/*
 * Configure the clocks, GPIO and other peripherals as required by the demo.
 */
static void prvSetupHardware( void );

static void prvSetupHardware( void )
{
    
    LEDS_Init();
    LEDS_Off(RED);
    LEDS_Off(BLUE);
    LEDS_Off(ORANGE);
    LEDS_Off(GREEN);
    LEDS_Off(RED2);
    LEDS_Off(GREEN2);

    Timer2_Init();
    
    return;    
}

void taskCreation(void)
{
   
    return;    
}

void queueCreation(void)
{
 
    return;    
}



int main(void)
{
    prvSetupHardware();
    
    queueCreation();
    
    taskCreation();
           
    __enable_irq();
    chSysInit();
    return 0;    
}
