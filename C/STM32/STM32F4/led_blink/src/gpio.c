
#include <libopencm3/stm32/f4/rcc.h>
#include <libopencm3/stm32/gpio.h>

void gpio_setup(void)
{
    /* Enable GPIOE clock. */
    /* Manually: */
    // RCC_AHB1ENR |= RCC_AHB1ENR_IOPDEN;
    /* Using API functions: */
    rcc_peripheral_enable_clock(&RCC_AHB1ENR, RCC_AHB1ENR_IOPDEN);

    /* Set GPIO12 (in GPIO port E) to 'output push-pull'. */
    /* Manually: */
    //GPIOE_CRH = (GPIO_CNF_OUTPUT_PUSHPULL << (((8 - 8) * 4) + 2));
    //GPIOE_CRH |= (GPIO_MODE_OUTPUT_2_MHZ << ((8 - 8) * 4));
    /* Using API functions: */
    gpio_mode_setup(GPIOE, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO12);
    gpio_mode_setup(GPIOE, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO13);
}
