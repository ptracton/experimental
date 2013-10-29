#include "stdio.h"
#include "string.h"
#include <stdint.h>

#include <stm32f30x.h>
#include <stm32f30x_rcc.h>
#include <stm32f30x_gpio.h>
#include <stm32f30x_usart.h>


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


int main(void)
{
    char i;    
    GPIO_InitTypeDef GPIO_A2;
    GPIO_InitTypeDef GPIO_A3;
    USART_InitTypeDef USART_2;    

    //
    // Turn on clock to the GPIO and UART
    //
    RCC_AHBPeriphClockCmd(RCC_AHBPeriph_GPIOA, ENABLE);
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
    GPIO_PinAFConfig(GPIOA, GPIO_PinSource2, GPIO_AF_7);

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
    GPIO_PinAFConfig(GPIOA, GPIO_PinSource3, GPIO_AF_7);

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

    __enable_irq();
    
    i=0;    
    while(1){
//	USART_SendData(USART2, 'A');	
//	i++;	
//	printf("print %d\n", i);	
    }
    

    return 0;    
}
