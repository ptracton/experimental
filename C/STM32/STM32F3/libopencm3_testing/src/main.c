#include <libopencm3/stm32/f3/rcc.h>
#include <libopencm3/stm32/gpio.h>

void gpio_setup(void)
{
    /* Enable GPIOE clock. */
    /* Manually: */
    // RCC_AHB1ENR |= RCC_AHB1ENR_IOPDEN;
    /* Using API functions: */
    rcc_peripheral_enable_clock(&RCC_AHBENR, RCC_AHBENR_IOPEEN);

    /* Set GPIO12 (in GPIO port E) to 'output push-pull'. */
    /* Manually: */
    //GPIOE_CRH = (GPIO_CNF_OUTPUT_PUSHPULL << (((8 - 8) * 4) + 2));
    //GPIOE_CRH |= (GPIO_MODE_OUTPUT_2_MHZ << ((8 - 8) * 4));
    /* Using API functions: */
    gpio_mode_setup(GPIOE, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO12);
    gpio_mode_setup(GPIOE, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO13);
}

int main(void)
{
    int i;

    gpio_setup();

    /* Blink the LED (PC8) on the board. */
    while (1) {
	/* Manually: */
	// GPIOD_BSRR = GPIO12;         /* LED off */
	// for (i = 0; i < 1000000; i++)        /* Wait a bit. */
	//      __asm__("nop");
	// GPIOD_BRR = GPIO9;           /* LED on */
	// for (i = 0; i < 1000000; i++)        /* Wait a bit. */
	//      __asm__("nop");

	/* Using API functions gpio_set()/gpio_clear(): */
	//gpio_set(GPIOE, GPIO9);       /* LED off */
	// for (i = 0; i < 1000000; i++)        /* Wait a bit. */
	//      __asm__("nop");
	//gpio_clear(GPIOE, GPIO9);     /* LED on */
	// for (i = 0; i < 1000000; i++)        /* Wait a bit. */
	//      __asm__("nop");

	/* Using API function gpio_toggle(): */
	gpio_toggle(GPIOE, GPIO12);     /* LED on/off */
	gpio_toggle(GPIOE, GPIO13);     /* LED on/off */
	for (i = 0; i < 2000000; i++) /* Wait a bit. */
	    __asm__("nop");

    }

    return 0;
}
