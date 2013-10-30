#include "stdio.h"
#include "string.h"
#include "stdint.h"

#include "stm32f30x.h"
#include <stm32f30x_usart.h>
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "task2.h"
#include "leds.h"
#include "syscalls.h"

xQueueHandle xTask2_Queue;

void Task2_Task( void *pvParameters )
{
    xTask2_Message xMessage;
    UNUSED(pvParameters);
    
    for (;;){
	while( xQueueReceive( xTask2_Queue, &xMessage, portMAX_DELAY ) != pdPASS );
	LEDS_Toggle(LED_2);
	if (xMessage.action !=0){
	    USART_SendData(USART2, '2');
	    //printf("Task 1 %d", xMessage.ptr);	    
	}
	
    }
    

    return;
}



