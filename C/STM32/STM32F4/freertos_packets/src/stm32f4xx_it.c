/**
  ******************************************************************************
  * @file    stm32f4xx_it.c
  * @author  MCD Application Team
  * @version V1.0.0
  * @date    19-September-2011
  * @brief   Main Interrupt Service Routines.
  *          This file provides all exceptions handler and peripherals interrupt
  *          service routine.
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, STMICROELECTRONICS SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  * <h2><center>&copy; COPYRIGHT 2011 STMicroelectronics</center></h2>
  ******************************************************************************
  */ 

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_it.h"
#include <stm32f4xx_tim.h>
#include <stm32f4xx_usart.h>
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "leds.h"
#include "task1.h"
#include "communication.h"
// #include "main.h"
// #include "usb_core.h"
// #include "usbd_core.h"
// #include "stm32f4_discovery.h"
// #include "usbd_hid_core.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/

/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

/* Private function prototypes -----------------------------------------------*/

/******************************************************************************/
/*            Cortex-M3 Processor Exceptions Handlers                         */
/******************************************************************************/

/**
  * @brief   This function handles NMI exception.
  * @param  None
  * @retval None
  */
void NMI_Handler(void)
{
}

/**
  * @brief  This function handles Hard Fault exception.
  * @param  None
  * @retval None
  */
void HardFault_Handler(void)
{
    LEDS_On(RED);
    LEDS_On(BLUE);
    LEDS_On(ORANGE);
    LEDS_On(GREEN);
    LEDS_On(RED2);
    LEDS_On(GREEN2);

  /* Go to infinite loop when Hard Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Memory Manage exception.
  * @param  None
  * @retval None
  */
void MemManage_Handler(void)
{
  /* Go to infinite loop when Memory Manage exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Bus Fault exception.
  * @param  None
  * @retval None
  */
void BusFault_Handler(void)
{
  /* Go to infinite loop when Bus Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles Usage Fault exception.
  * @param  None
  * @retval None
  */
void UsageFault_Handler(void)
{
  /* Go to infinite loop when Usage Fault exception occurs */
  while (1)
  {
  }
}

/**
  * @brief  This function handles SVCall exception.
  * @param  None
  * @retval None
  */
void SVC_Handler(void)
{
}

/**
  * @brief  This function handles Debug Monitor exception.
  * @param  None
  * @retval None
  */
void DebugMon_Handler(void)
{
}

/**
  * @brief  This function handles PendSVC exception.
  * @param  None
  * @retval None
  */
void PendSV_Handler(void)
{
}

/**
  * @brief  This function handles SysTick Handler.
  * @param  None
  * @retval None
  */
void SysTick_Handler(void)
{

  
}

/******************************************************************************/
/*                 STM32Fxxx Peripherals Interrupt Handlers                   */
/*  Add here the Interrupt Handler for the used peripheral(s) (PPP), for the  */
/*  available peripheral interrupt handler's name please refer to the startup */
/*  file (startup_stm32fxxx.s).                                               */
/******************************************************************************/

/**
  * @brief  This function handles TIM2_IRQ Handler.  Toggle LED and send OS message
  * @param  None
  * @retval None
  */
void TIM2_IRQHandler(void)
{
    xTask1_Message xMessage;
    portBASE_TYPE xHigherPriorityTaskWoken = pdFALSE;
    portBASE_TYPE retval;
    
    LEDS_Toggle(ORANGE);
      
    //
    // Clear the timer
    //
    TIM_ClearFlag(TIM2, TIM_SR_UIF);

    //
    // Clear the interrupt at the NVIC level
    //
    NVIC_ClearPendingIRQ(TIM2_IRQn);

    
    xMessage.character = 0xA;
    retval = xQueueSendFromISR( xTask1_Queue, &xMessage, &xHigherPriorityTaskWoken );
    if (retval != pdTRUE){
	LEDS_On(RED);	    
    }	  
}

/**
  * @brief  This function handles USART2_IRQ Handler.  
  * @param  None
  * @retval None
  */
void USART2_IRQHandler(void)
{
    portBASE_TYPE retval;    
    portBASE_TYPE xHigherPriorityTaskWoken = pdFALSE;
    uint16_t data;
    static xCommunication_Message xMessage;
    static uint8_t data_count;
    static uint8_t state =0;
    
    //
    // If the RX Not Empty bit is set grab the byte
    // 
    if (USART_GetITStatus(USART2, USART_IT_RXNE) == SET){	
	data = USART_ReceiveData(USART2);
    }
 
    //
    // Create the packet and when ready send to task via OS
    // 
    switch(state){
    case 0: 
	xMessage.packet.type = data;	
	state = 1;	
	break;
    case 1:
	xMessage.packet.size = data;
	data_count = 0;	
	
	if (xMessage.packet.size){
	    state = 2;
	}else{
	    state = 3;
	}
	
	
	break;
    case 2:
	if (data_count < (xMessage.packet.size-1)){
	    xMessage.packet.data[data_count] = data;
	    data_count ++;	    
	}else{
	    data_count =0;
	    state = 3;
	}		
	break;
    case 3:
	if (data_count <3 ){
	    xMessage.packet.crc = data << (data_count << 2);
	    data_count ++;	    
	}else{
	    data_count =0;
	    state = 0;
	    //
	    // Send the byte to the OS
	    //
	    xMessage.tx_or_rx = RECEIVE_DATA;
	    retval = xQueueSendFromISR( xCommunication_Queue, &xMessage, &xHigherPriorityTaskWoken );
	    if (retval != pdTRUE){
		LEDS_On(RED);	    
	    }
	}			
	break;
    default:
	state = 0;
	data_count = 0;	
	break;       
    }
   
    //
    // Clear the interrupt at the NVIC level
    //
    NVIC_ClearPendingIRQ(USART2_IRQn);

    return;
}

/******************* (C) COPYRIGHT 2011 STMicroelectronics *****END OF FILE****/
