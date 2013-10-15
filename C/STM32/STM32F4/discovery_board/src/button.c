
#include "stm32f4_discovery_board.h"
#include "libopencm3/stm32/f4/gpio.h"  
#include "libopencm3/stm32/f4/rcc.h"  
#include "button.h"


void BUTTON_Init(void)
{
    /* Enable GPIOA clock. */
    rcc_peripheral_enable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPAEN);
    
    /* Set GPIO0 (in GPIO port A) to 'input open-drain'. */
    gpio_mode_setup(GPIOA, GPIO_MODE_INPUT, GPIO_PUPD_NONE, BUTTON_USER);
    
    return;    
}
