
#ifndef __LEDS_H__
#define __LEDS_H__

typedef enum{
    LED_0 = (0x0100u),
    LED_1 = (0x0200u),
    LED_2 = (0x0400u),
    LED_3 = (0x0800u),
    LED_4 = (0x1000u),
    LED_5 = (0x2000u),
    LED_6 = (0x4000u),
    LED_7 = (0x8000u)
}LEDS_ENUM;


void LEDS_Init(void);
void LEDS_Shutdown(void);
void LEDS_On(LEDS_ENUM led);
void LEDS_Off(LEDS_ENUM led);
void LEDS_Toggle(LEDS_ENUM led);


#endif

