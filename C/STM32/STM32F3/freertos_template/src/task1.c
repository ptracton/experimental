#include "stdio.h"
#include "string.h"
#include "stdint.h"

#include "stm32f30x.h"
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "task1.h"
#include "task2.h"
#include "leds.h"
#include "syscalls.h"

xQueueHandle xTask1_Queue;

void Task1_Task( void *pvParameters )
{
    xTask1_Message xMessage;
    UNUSED(pvParameters);
    
    for (;;){
	while( xQueueReceive( xTask1_Queue, &xMessage, portMAX_DELAY ) != pdPASS );
	LEDS_Toggle(LED_1);
	xMessage.action = 0xAA;
	xMessage.ptr = 0xDEADBEEF;
	xQueueSend( xTask2_Queue, &xMessage, 100 );
	
    }
    

    return;
}


