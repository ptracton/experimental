#include <libopencm3/stm32/rcc.h>


static void SetSysClock(void);

uint32_t SystemCoreClock = 168000000;

static void SetSysClock(void)
{
    rcc_clock_setup_hse_3v3(&hse_8mhz_3v3[CLOCK_3V3_168MHZ]);
    return;    
}


void SystemInit(void)
{
    SetSysClock();    
    return;    
}

void SystemCoreClockUpdate(void)
{
    return;    
}

