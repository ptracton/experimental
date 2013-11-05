
#ifndef __LEDS_H__
#define __LEDS_H__

#include <stm32f4xx_gpio.h>

typedef enum{
    RED2   =  GPIO_Pin_5,
    GREEN  =  GPIO_Pin_12,
    ORANGE =  GPIO_Pin_13,
    RED    =  GPIO_Pin_14,
    BLUE   =  GPIO_Pin_15,
    GREEN2 =  GPIO_Pin_9    //On GPIO A!        
} LEDS;

#define IS_LED(LED) (((LED) == RED2)   || \
		     ((LED) == GREEN)  || \
		     ((LED) == ORANGE) || \
		     ((LED) == RED)    || \
		     ((LED) == BLUE)   || \
		     ((LED) == GREEN2))
void LEDS_Init(void);
void LEDS_On(LEDS led);
void LEDS_Off(LEDS led);
void LEDS_Toggle(LEDS led);


#endif
