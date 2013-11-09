#include <stm32f4xx.h>
#include "ch.h"
#include "timer2.h"
#include "leds.h"
#include "thread1.h"

extern WORKING_AREA(Thread1Area, 128);
extern Thread * Thread1_ptr;

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
    Thread1_ptr = chThdCreateStatic(Thread1Area,
				    sizeof(Thread1Area),
				    NORMALPRIO,    /* Initial priority.    */
				    Thread1,      /* Thread function.     */
				    NULL);         /* Thread parameter.    */
    
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

    while (TRUE){

    }
    
    
    return 0;    
}
