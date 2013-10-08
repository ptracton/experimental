#include <libopencm3/stm32/gpio.h>
#include "gpio.h"


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
