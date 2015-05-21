#include "stdio.h"
#include "string.h"
#include <stdint.h>

#include <stm32f30x.h>
#include <stm32f30x_rcc.h>
#include <stm32f30x_gpio.h>
#include <stm32f30x_usart.h>
#include "usart2.h"



int main(void)
{

    USART2_Init();
    
    __enable_irq();
    
    while(1){
      // uartPutch('P');
      // uartPutch('y');
      // uartPutch('t');
      // uartPutch('h');
      // uartPutch('o');
      // uartPutch('n');
      // uartPutch('\n');
    }
    

    return 0;    
}
