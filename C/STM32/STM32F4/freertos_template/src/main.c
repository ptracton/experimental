#include <stm32f4xx.h>
#include <FreeRTOS.h>
#include <task.h>
#include "queue.h"
#include "timer2.h"
#include "leds.h"
#include "task1.h"

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
    portBASE_TYPE retval;
    
    retval = xTaskCreate( Task1_Task, ( signed portCHAR * ) "TASK1",  Task1_STACK_SIZE, NULL, tskIDLE_PRIORITY+1, NULL );
    if (retval != pdPASS){
	LEDS_On(RED);
	LEDS_On(GREEN);
	while(1);	
    }
    return;    
}

void queueCreation(void)
{
    xTask1_Queue = xQueueCreate( Task1_QUEUE_SIZE, sizeof( xTask1_Message ) );
    if ( xTask1_Queue == 0 ){
	LEDS_On(RED2);
	LEDS_On(GREEN2);
	while(1);	
    }
    return;    
}



int main(void)
{
    prvSetupHardware();
    
    queueCreation();
    
    taskCreation();
           
    __enable_irq();
    vTaskStartScheduler();
    return 0;    
}
