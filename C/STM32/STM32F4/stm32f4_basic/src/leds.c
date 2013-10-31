
#include <stm32f4xx_gpio.h>
#include <stm32f4xx_rcc.h>
#include "leds.h"

void LEDS_Init(void)
{
    GPIO_InitTypeDef gpio;
    
    //
    // Turn on clock to GPIO D
    //
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE);
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
    
    //
    // Set up GPIO to be a fast output and push/pull.
    //
    GPIO_StructInit(&gpio);    
    gpio.GPIO_Mode= GPIO_Mode_OUT;
    gpio.GPIO_Speed =  GPIO_Speed_50MHz;
    gpio.GPIO_OType = GPIO_OType_PP;
    gpio.GPIO_PuPd = GPIO_PuPd_NOPULL;

    gpio.GPIO_Pin = GREEN;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = ORANGE;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = RED;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = BLUE;
    GPIO_Init(GPIOD, &gpio);

    gpio.GPIO_Pin = RED2;
    GPIO_Init(GPIOD, &gpio);

    //
    // NOTE THIS IS GPIO A!!!
    //
    gpio.GPIO_Pin = GREEN2;
    GPIO_Init(GPIOA, &gpio);
}

void LEDS_On(LEDS led)
{
    if (IS_LED(led)){
	if (led == GREEN2){
	    GPIO_SetBits(GPIOD, led);	    
	}else{
	    GPIO_SetBits(GPIOA, led);	    
	}    
    }    
    return;    
}

void LEDS_Off(LEDS led)
{
    if (IS_LED(led)){
	if (led == GREEN2){
	    GPIO_ResetBits(GPIOD, led);	    
	}else{
	    GPIO_ResetBits(GPIOA, led);	    
	}    
    }    
    return;    
}

void LEDS_Toggle(LEDS led)
{
    if (IS_LED(led)){
	if (led == GREEN2){
	    GPIO_ToggleBits(GPIOD, led);	    
	}else{
	    GPIO_ToggleBits(GPIOA, led);	    
	}    
    }    
    return;    
}
