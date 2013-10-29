#include <stm32f30x.h>
#include <FreeRTOS.h>
#include <task.h>
#include "queue.h"

#include "leds.h"
#include "usart2.h"
#include "task1.h"
#include "task2.h"


/*
 * Configure the clocks, GPIO and other peripherals as required by the demo.
 */
static void prvSetupHardware( void );

static void prvSetupHardware( void )
{
    
    LEDS_Init();
    USART2_Init();
    return;    
}

void taskCreation(void)
{
    xTaskCreate( Task1_Task, ( signed portCHAR * ) "TASK1",  Task1_STACK_SIZE, NULL, tskIDLE_PRIORITY+1, NULL );
    xTaskCreate( Task2_Task, ( signed portCHAR * ) "TASK1",  Task2_STACK_SIZE, NULL, tskIDLE_PRIORITY+2, NULL );
}

void queueCreation(void)
{
    xTask1_Queue = xQueueCreate( Task1_QUEUE_SIZE, sizeof( xTask1_Message ) );
}



int main(void)
{
    prvSetupHardware();
    
    taskCreation();
        

    vTaskStartScheduler();
    return 0;    
}
