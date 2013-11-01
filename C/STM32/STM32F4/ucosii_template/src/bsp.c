#include <stm32f4xx_conf.h>
#include "includes.h"
#include "leds.h"

void BSP_Init(void)
{
    NVIC_InitTypeDef NVIC_InitStructure;
    TIM_TimeBaseInitTypeDef timer; 
    
    LEDS_Init();    

    //
    // Turn on Timer 2
    //
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    
    TIM_TimeBaseStructInit(&timer);  
    timer.TIM_Period = 16800000;
    timer.TIM_Prescaler = TIM_ICPSC_DIV1;
    timer.TIM_ClockDivision = TIM_CKD_DIV1;
    timer.TIM_CounterMode = TIM_CounterMode_Down;  
    TIM_TimeBaseInit(TIM2, &timer);

    //
    // Turn on Timer 2 IRQ
    //
    NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    /* Prescaler configuration */
    TIM_PrescalerConfig(TIM2, 0, TIM_PSCReloadMode_Immediate);
    
    /* TIM Interrupts enable */
    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);
    
    /* TIM3 enable counter */
    TIM_Cmd(TIM2, ENABLE);

    return;    
}
