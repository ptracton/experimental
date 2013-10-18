#include <stm32f30x.h>
#include <stm32f30x_rcc.h>
#include <stm32f30x_tim.h>
#include <stm32f30x_misc.h>
#include "leds.h"

#define WAIT_1SECOND 8000000

void Wait(uint32_t time)
{
    volatile uint32_t i;
    for (i=0; i<time; i++);
    return;    
}

int main(void)
{
    NVIC_InitTypeDef NVIC_InitStructure;
    TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
    uint16_t PrescalerValue = 0;
    
    LEDS_Init();
    
    /* TIM3 clock enable */
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);
    
    /* Enable the TIM3 gloabal Interrupt */
    NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
    
    /* Compute the prescaler value */
    PrescalerValue = (uint16_t) ((SystemCoreClock) / 72000000) - 1;
    
    /* Time base configuration */
    TIM_TimeBaseStructure.TIM_Period = 65535;
    TIM_TimeBaseStructure.TIM_Prescaler = 0;
    TIM_TimeBaseStructure.TIM_ClockDivision = 0;
    TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
    
    TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

    /* Prescaler configuration */
    TIM_PrescalerConfig(TIM3, PrescalerValue, TIM_PSCReloadMode_Immediate);
    
    /* TIM Interrupts enable */
    TIM_ITConfig(TIM3, TIM_IT_CC1 | TIM_IT_CC2 | TIM_IT_CC3 | TIM_IT_CC4, ENABLE);
    
    /* TIM3 enable counter */
    TIM_Cmd(TIM3, ENABLE);

    __enable_irq();

    while(1){
	LEDS_Toggle(LED_1);
	Wait(WAIT_1SECOND);
    }
    

    return 0;    
}
