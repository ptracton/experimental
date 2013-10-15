

#ifndef __LEDS_H__
#define __LEDS_H__

//
// Must include #include "libopencm3/stm32/f4/gpio.h" before this file
//

#define LED_GREEN  GPIO12
#define LED_ORANGE GPIO13
#define LED_RED    GPIO14
#define LED_BLUE   GPIO15

void LED_Init(void);
void LED_Disable(void);

void LED_Toggle(uint16_t gpios);

#endif

