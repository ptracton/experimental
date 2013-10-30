#include <stm32f30x.h>
#include <stm32f30x_rcc.h>
#include <stm32f30x_tim.h>
#include <stm32f30x_misc.h>


void Timer2_Init(void)
{
    NVIC_InitTypeDef NVIC_InitStructure;
    TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
    uint16_t PrescalerValue = 0;

    /* TIM3 clock enable */
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    
    /* Enable the TIM3 gloabal Interrupt */
    NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
    
    /* Compute the prescaler value */
    PrescalerValue = 0;//(uint16_t) ((SystemCoreClock) / 72000000) - 1;
    
    /* Time base configuration */
    TIM_TimeBaseStructInit(&TIM_TimeBaseStructure);    
    TIM_TimeBaseStructure.TIM_Period = 72000000;
    TIM_TimeBaseStructure.TIM_Prescaler = TIM_ICPSC_DIV1;
    TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;
    TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Down;
    
    TIM_TimeBaseInit(TIM2, &TIM_TimeBaseStructure);

    /* Prescaler configuration */
    TIM_PrescalerConfig(TIM2, PrescalerValue, TIM_PSCReloadMode_Immediate);
    
    /* TIM Interrupts enable */
    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);
    
    /* TIM3 enable counter */
    TIM_Cmd(TIM2, ENABLE);
    return;    
}
