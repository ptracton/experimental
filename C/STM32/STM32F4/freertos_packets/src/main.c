#include <stm32f4xx.h>
#include <stm32f4xx_rcc.h>
#include <stm32f4xx_gpio.h>
#include <stm32f4xx_usart.h>
#include <FreeRTOS.h>
#include <task.h>
#include "queue.h"
#include "timer2.h"
#include "leds.h"
#include "task1.h"
#include "communication.h"

/*
 * Configure the clocks, GPIO and other peripherals as required by the demo.
 */
static void prvSetupHardware( void );
static void prvUSART_Init(void);

int uartPutch(int ch)
{
    static int last;

    if ((ch == (int)'\n') && (last != (int)'\r'))
    {
	last = (int)'\r';

	while(USART_GetFlagStatus(USART2, USART_FLAG_TXE) == RESET);

	USART_SendData(USART2, last);
    }
    else
	last = ch;

    while(USART_GetFlagStatus(USART2, USART_FLAG_TXE) == RESET);

    USART_SendData(USART2, ch);

    return(ch);
}


static void prvUSART_Init(void)
{
    GPIO_InitTypeDef GPIO_A2;
    GPIO_InitTypeDef GPIO_A3;
    USART_InitTypeDef USART_2;    

    //
    // Turn on clock to the GPIO and UART
    //
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);
        
    //
    // GPIO Pin 2 is USART 2 TX.  Configure it into Alternate Function Mode
    //
    GPIO_StructInit(&GPIO_A2);    
    GPIO_A2.GPIO_Pin = GPIO_Pin_2;
    GPIO_A2.GPIO_Mode =  GPIO_Mode_AF;
    GPIO_A2.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_A2.GPIO_OType = GPIO_OType_PP;
    GPIO_A2.GPIO_PuPd = GPIO_PuPd_UP;
    GPIO_Init(GPIOA, &GPIO_A2);    
    GPIO_PinAFConfig(GPIOA, GPIO_PinSource2, GPIO_AF_USART2);

    //
    // GPIO Pin 3 is USART 2 RX.  Configure it into Alternate Function Mode
    //    
    GPIO_StructInit(&GPIO_A3);    
    GPIO_A3.GPIO_Pin = GPIO_Pin_3;
    GPIO_A3.GPIO_Mode =  GPIO_Mode_AF;
    GPIO_A3.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_A3.GPIO_OType = GPIO_OType_PP;
    GPIO_A3.GPIO_PuPd = GPIO_PuPd_UP;
    GPIO_Init(GPIOA, &GPIO_A3);    
    GPIO_PinAFConfig(GPIOA, GPIO_PinSource3, GPIO_AF_USART2);

    //
    // Configure UART2
    //
    USART_StructInit(&USART_2);
    USART_2.USART_BaudRate = 115200;
    USART_2.USART_WordLength =  USART_WordLength_8b;
    USART_2.USART_StopBits = USART_StopBits_1;
    USART_2.USART_Parity = USART_Parity_No;
    USART_2.USART_Mode = USART_Mode_Rx  | USART_Mode_Tx ;
    USART_Init(USART2, &USART_2);

    //
    // Interrupt on RX Not Empty
    //
    USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);
    NVIC_EnableIRQ(USART2_IRQn);
     
    //
    // Enable the USART block
    //
    USART_Cmd(USART2, ENABLE); 
    
    return;
}

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
    prvUSART_Init();
    
    return;    
}

void taskCreation(void)
{
    portBASE_TYPE retval;
    
    retval = xTaskCreate( Task1_Task, ( signed portCHAR * ) "TASK1",  Task1_STACK_SIZE, NULL, tskIDLE_PRIORITY+1, NULL );
    if (retval != pdPASS){
	while(1);	
    }

    
    retval = xTaskCreate( vCommunication_Task, ( signed portCHAR * ) "Communication",  COMMUNICATION_STACK_SIZE, NULL, tskIDLE_PRIORITY+2, NULL );
    if (retval != pdPASS){
	while(1);	
    }

    return;    
}

void queueCreation(void)
{
    xTask1_Queue = xQueueCreate( Task1_QUEUE_SIZE, sizeof( xTask1_Message ) );
    if ( xTask1_Queue == 0 ){
	while(1);	
    }

    xCommunication_Queue = xQueueCreate( COMMUNICATION_QUEUE_SIZE, sizeof( xCommunication_Message ) );
    if ( xCommunication_Queue == 0 ){
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
