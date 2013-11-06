#include <stm32f30x.h>
#include <stm32f30x_rcc.h>
#include <stm32f30x_gpio.h>
#include "leds.h"


void LEDS_Init(void)
{
    GPIO_InitTypeDef gpioE;
    
    //
    // Turn on clocks to GPIO E so we can drive the outputs
    //
    RCC_AHBPeriphClockCmd(RCC_AHBPeriph_GPIOE, ENABLE);
    
    //
    // Set up default values
    //
    GPIO_StructInit(&gpioE);
    
    //
    // Make pins 8-15 outputs since they are connected to the LEDS
    //
    gpioE.GPIO_Pin = GPIO_Pin_8 | GPIO_Pin_9 | GPIO_Pin_10 | GPIO_Pin_11 | GPIO_Pin_12 | GPIO_Pin_13 |GPIO_Pin_14 | GPIO_Pin_15;
    gpioE.GPIO_Mode = GPIO_Mode_OUT;
    
    //
    // Initialize the hardware
    //
    GPIO_Init(GPIOE, &gpioE);
        
    return;    
}

void LEDS_Shutdown(void)
{
    return;    
}

void LEDS_On(LEDS_ENUM led)
{
    GPIOE->ODR |= led;    
    return;    
}

void LEDS_Off(LEDS_ENUM led)
{
    GPIOE->ODR &= ~led;
    return;    
}

void LEDS_Toggle(LEDS_ENUM led)
{
    GPIOE->ODR ^= led;    
    return;    
}





