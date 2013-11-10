#include "stdio.h"
#include "string.h"
#include "stdint.h"

#include "stm32f30x.h"
#include <stm32f30x_usart.h>

#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#include "CLI_Task.h"
#include "leds.h"
#include "syscalls.h"

xQueueHandle xCLI_Queue;


void vCLI_Task(void * pvParameters)
{
    xCLI_Message xMessage;
    printf("CLI Task Up\r\n");
    
    for (;;){
	while( xQueueReceive( xCLI_Queue, &xMessage, portMAX_DELAY ) != pdPASS );


	USART_SendData(USART2, xMessage.character);	
	LEDS_Toggle(LED_3);
    }
    
    return;
}
