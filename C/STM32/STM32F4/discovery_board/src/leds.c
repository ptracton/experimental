

#include "stm32f4_discovery_board.h"
#include "libopencm3/stm32/f4/gpio.h"  
#include "libopencm3/stm32/f4/rcc.h"  
#include "leds.h"


void LED_Init(void)
{
    /* Enable GPIOD clock. */
    rcc_peripheral_enable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPDEN);
    
    /* Set GPIO12 (in GPIO port D) to 'output push-pull'. */
    gpio_mode_setup(GPIOD, GPIO_MODE_OUTPUT,
                    GPIO_PUPD_NONE, LED_GREEN | LED_ORANGE | LED_RED | LED_BLUE);
    
    return;    
}

void LED_Disable(void)
{
    rcc_peripheral_disable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPDEN);
    return;    
}


void LED_Toggle(uint16_t gpios)
{
    gpio_toggle(GPIOD, gpios);
    return;    
}


