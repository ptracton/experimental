#include <stm32f30x.h>
#include <FreeRTOS.h>
#include <task.h>
#include "queue.h"

#include "leds.h"
#include "usart2.h"
#include "task1.h"

/*
 * Configure the clocks, GPIO and other peripherals as required by the demo.
 */
static void prvSetupHardware( void );

static void prvSetupHardware( void )
{
    
    LEDS_Init();
    LEDS_Off(LED_5);
    LEDS_Off(LED_4);

    Timer2_Init();
    
    return;    
}

void taskCreation(void)
{
    portBASE_TYPE retval;
    
    retval = xTaskCreate( Task1_Task, ( signed portCHAR * ) "TASK1",  Task1_STACK_SIZE, NULL, tskIDLE_PRIORITY+1, NULL );
    if (retval != pdPASS){
	LEDS_On(LED_0);
	LEDS_On(LED_1);
//	while(1);	
    }
    return;    
}

void queueCreation(void)
{
    xTask1_Queue = xQueueCreate( Task1_QUEUE_SIZE, sizeof( xTask1_Message ) );
    if ( xTask1_Queue == 0 ){
	LEDS_On(LED_2);
	LEDS_On(LED_3);
//	while(1);	
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
