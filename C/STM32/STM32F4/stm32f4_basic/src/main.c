#include <stm32f4xx_conf.h>
#include "leds.h"

#define WAIT_1SECOND 16000000

void Wait(uint32_t time)
{
    volatile uint32_t i;
    for (i=0; i<time; i++);
    return;    
}

int main(void)
{
    GPIO_InitTypeDef gpio;
    
    //
    // Turn on clock to GPIO D
    //
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE);
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
    
    GPIO_StructInit(&gpio);    
    gpio.GPIO_Pin = GPIO_Pin_12;
    gpio.GPIO_Mode= GPIO_Mode_OUT;
    gpio.GPIO_Speed =  GPIO_Speed_50MHz;
    gpio.GPIO_OType = GPIO_OType_PP;
    gpio.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = GPIO_Pin_13;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = GPIO_Pin_14;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = GPIO_Pin_15;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = GPIO_Pin_5;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = GPIO_Pin_9;
    GPIO_Init(GPIOA, &gpio);
    
    while(1){
	LEDS_Toggle(GREEN);    
	Wait(WAIT_1SECOND);
	LEDS_Toggle(ORANGE);    
	Wait(WAIT_1SECOND);
	LEDS_Toggle(RED);    
	Wait(WAIT_1SECOND);
	LEDS_Toggle(BLUE);    
	Wait(WAIT_1SECOND);
	LEDS_Toggle(GREEN2);   
	Wait(WAIT_1SECOND);
	LEDS_Toggle(RED2);
	
	Wait(WAIT_1SECOND);
    }         

    return 0;    
}
