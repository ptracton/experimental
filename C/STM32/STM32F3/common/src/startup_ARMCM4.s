/* File: startup_ARMCM4.S
 * Purpose: startup file for Cortex-M4 devices. Should use with 
 *   GCC for ARM Embedded Processors
 * Version: V1.4
 * Date: 09 July 2012
 * 
 * Copyright (c) 2011, 2012, ARM Limited
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the ARM Limited nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL ARM LIMITED BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
    .syntax unified
    .arch armv7-m

    .section .stack
    .align 3
#ifdef __STACK_SIZE
    .equ    Stack_Size, __STACK_SIZE
#else
    .equ    Stack_Size, 0xc00
#endif
    .globl    __StackTop
    .globl    __StackLimit
__StackLimit:
    .space    Stack_Size
    .size __StackLimit, . - __StackLimit
__StackTop:
    .size __StackTop, . - __StackTop

    .section .heap
    .align 3
#ifdef __HEAP_SIZE
    .equ    Heap_Size, __HEAP_SIZE
#else
    .equ    Heap_Size, 0
#endif
    .globl    __HeapBase
    .globl    __HeapLimit
__HeapBase:
    .if    Heap_Size
    .space    Heap_Size
    .endif
    .size __HeapBase, . - __HeapBase
__HeapLimit:
    .size __HeapLimit, . - __HeapLimit
    
    .section .isr_vector
    .align 2
    .globl __isr_vector
__isr_vector:
    .long    __StackTop            /* Top of Stack */
    .long    Reset_Handler         /* Reset Handler */
    .long    NMI_Handler           /* NMI Handler */
    .long    HardFault_Handler     /* Hard Fault Handler */
    .long    MemManage_Handler     /* MPU Fault Handler */
    .long    BusFault_Handler      /* Bus Fault Handler */
    .long    UsageFault_Handler    /* Usage Fault Handler */
    .long    0                     /* Reserved */
    .long    0                     /* Reserved */
    .long    0                     /* Reserved */
    .long    0                     /* Reserved */
    .long    SVC_Handler           /* SVCall Handler */
    .long    DebugMon_Handler      /* Debug Monitor Handler */
    .long    0                     /* Reserved */
    .long    PendSV_Handler        /* PendSV Handler */
    .long    SysTick_Handler       /* SysTick Handler */
	.long	WWDG_IRQHandler
	.long	PVD_IRQHandler
	.long	TAMPER_STAMP_IRQHandler
	.long	RTC_WKUP_IRQHandler
	.long	FLASH_IRQHandler
	.long	RCC_IRQHandler
	.long	EXTI0_IRQHandler
	.long	EXTI1_IRQHandler
	.long	EXTI2_TS_IRQHandler
	.long	EXTI3_IRQHandler
	.long	EXTI4_IRQHandler
	.long	DMA1_Channel1_IRQHandler
	.long	DMA1_Channel2_IRQHandler
	.long	DMA1_Channel3_IRQHandler
	.long	DMA1_Channel4_IRQHandler
	.long	DMA1_Channel5_IRQHandler
	.long	DMA1_Channel6_IRQHandler
	.long	DMA1_Channel7_IRQHandler
	.long	ADC1_2_IRQHandler
	.long	USB_HP_CAN1_TX_IRQHandler
	.long	USB_LP_CAN1_RX0_IRQHandler
	.long	CAN1_RX1_IRQHandler
	.long	CAN1_SCE_IRQHandler
	.long	EXTI9_5_IRQHandler
	.long	TIM1_BRK_TIM15_IRQHandler
	.long	TIM1_UP_TIM16_IRQHandler
	.long	TIM1_TRG_COM_TIM17_IRQHandler
	.long	TIM1_CC_IRQHandler
	.long	TIM2_IRQHandler
	.long	TIM3_IRQHandler
	.long	TIM4_IRQHandler
	.long	I2C1_EV_IRQHandler
	.long	I2C1_ER_IRQHandler
	.long	I2C2_EV_IRQHandler
	.long	I2C2_ER_IRQHandler
	.long	SPI1_IRQHandler
	.long	SPI2_IRQHandler
	.long	USART1_IRQHandler
	.long	USART2_IRQHandler
	.long	USART3_IRQHandler
	.long	EXTI15_10_IRQHandler
	.long	RTC_Alarm_IRQHandler
	.long	USBWakeUp_IRQHandler
	.long	TIM8_BRK_IRQHandler
	.long	TIM8_UP_IRQHandler
	.long	TIM8_TRG_COM_IRQHandler
	.long	TIM8_CC_IRQHandler
	.long	ADC3_IRQHandler
	.long	0
	.long	0
	.long	0
	.long	SPI3_IRQHandler
	.long	UART4_IRQHandler
	.long	UART5_IRQHandler
	.long	TIM6_DAC_IRQHandler
	.long	TIM7_IRQHandler
	.long	DMA2_Channel1_IRQHandler
	.long	DMA2_Channel2_IRQHandler
	.long	DMA2_Channel3_IRQHandler
	.long	DMA2_Channel4_IRQHandler
	.long	DMA2_Channel5_IRQHandler
	.long	ADC4_IRQHandler
	.long	0
	.long	0
	.long	COMP1_2_3_IRQHandler
	.long	COMP4_5_6_IRQHandler
	.long	COMP7_IRQHandler
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	0
	.long	USB_HP_IRQHandler
	.long	USB_LP_IRQHandler
	.long	USBWakeUp_RMP_IRQHandler
	.long	0
	.long	0
	.long	0
	.long	0
	.long	FPU_IRQHandler

    /* External interrupts */
    .long    Default_Handler
    
    .size    __isr_vector, . - __isr_vector

    .text
    .thumb
    .thumb_func
    .align 2
    .globl    Reset_Handler
    .type    Reset_Handler, %function
Reset_Handler:
/*     Loop to copy data from read only memory to RAM. The ranges
 *      of copy from/to are specified by following symbols evaluated in 
 *      linker script.
 *      __etext: End of code section, i.e., begin of data sections to copy from.
 *      __data_start__/__data_end__: RAM address range that data should be
 *      copied to. Both must be aligned to 4 bytes boundary.  */

    ldr    r1, =__etext
    ldr    r2, =__data_start__
    ldr    r3, =__data_end__

#if 1
/* Here are two copies of loop implemenations. First one favors code size
 * and the second one favors performance. Default uses the first one. 
 * Change to "#if 0" to use the second one */
.LC0:
    cmp     r2, r3
    ittt    lt
    ldrlt   r0, [r1], #4
    strlt   r0, [r2], #4
    blt    .LC0
#else
    subs    r3, r2
    ble    .LC1    
.LC0:
    subs    r3, #4
    ldr    r0, [r1, r3]
    str    r0, [r2, r3]
    bgt    .LC0
.LC1:
#endif

#ifdef __STARTUP_CLEAR_BSS
/*     This part of work usually is done in C library startup code. Otherwise,
 *     define this macro to enable it in this startup.
 *
 *     Loop to zero out BSS section, which uses following symbols
 *     in linker script:
 *      __bss_start__: start of BSS section. Must align to 4
 *      __bss_end__: end of BSS section. Must align to 4
 */
    ldr r1, =__bss_start__
    ldr r2, =__bss_end__

    movs    r0, 0
.LC2:
    cmp     r1, r2
    itt    lt
    strlt   r0, [r1], #4
    blt    .LC2
#endif /* __STARTUP_CLEAR_BSS */

#ifndef __NO_SYSTEM_INIT
    bl    SystemInit
#endif

#ifndef __START
#define __START _start
#endif
    bl    __START
    .pool
    .size Reset_Handler, . - Reset_Handler
    
/*    Macro to define default handlers. Default handler
 *    will be weak symbol and just dead loops. They can be
 *    overwritten by other handlers */
    .macro    def_default_handler    handler_name
    .align 1
    .thumb_func
    .weak    \handler_name
    .type    \handler_name, %function
\handler_name :
    b    .
    .size    \handler_name, . - \handler_name
    .endm
    
    def_default_handler    NMI_Handler
    def_default_handler    HardFault_Handler
    def_default_handler    MemManage_Handler
    def_default_handler    BusFault_Handler
    def_default_handler    UsageFault_Handler
    def_default_handler    SVC_Handler
    def_default_handler    DebugMon_Handler
    def_default_handler    PendSV_Handler
    def_default_handler    SysTick_Handler
	def_default_handler	WWDG_IRQHandler
	def_default_handler	PVD_IRQHandler
	def_default_handler	TAMPER_STAMP_IRQHandler
	def_default_handler	RTC_WKUP_IRQHandler
	def_default_handler	FLASH_IRQHandler
	def_default_handler	RCC_IRQHandler
	def_default_handler	EXTI0_IRQHandler
	def_default_handler	EXTI1_IRQHandler
	def_default_handler	EXTI2_TS_IRQHandler
	def_default_handler	EXTI3_IRQHandler
	def_default_handler	EXTI4_IRQHandler
	def_default_handler	DMA1_Channel1_IRQHandler
	def_default_handler	DMA1_Channel2_IRQHandler
	def_default_handler	DMA1_Channel3_IRQHandler
	def_default_handler	DMA1_Channel4_IRQHandler
	def_default_handler	DMA1_Channel5_IRQHandler
	def_default_handler	DMA1_Channel6_IRQHandler
	def_default_handler	DMA1_Channel7_IRQHandler
	def_default_handler	ADC1_2_IRQHandler
	def_default_handler	USB_HP_CAN1_TX_IRQHandler
	def_default_handler	USB_LP_CAN1_RX0_IRQHandler
	def_default_handler	CAN1_RX1_IRQHandler
	def_default_handler	CAN1_SCE_IRQHandler
	def_default_handler	EXTI9_5_IRQHandler
	def_default_handler	TIM1_BRK_TIM15_IRQHandler
	def_default_handler	TIM1_UP_TIM16_IRQHandler
	def_default_handler	TIM1_TRG_COM_TIM17_IRQHandler
	def_default_handler	TIM1_CC_IRQHandler
	def_default_handler	TIM2_IRQHandler
	def_default_handler	TIM3_IRQHandler
	def_default_handler	TIM4_IRQHandler
	def_default_handler	I2C1_EV_IRQHandler
	def_default_handler	I2C1_ER_IRQHandler
	def_default_handler	I2C2_EV_IRQHandler
	def_default_handler	I2C2_ER_IRQHandler
	def_default_handler	SPI1_IRQHandler
	def_default_handler	SPI2_IRQHandler
	def_default_handler	USART1_IRQHandler
	def_default_handler	USART2_IRQHandler
	def_default_handler	USART3_IRQHandler
	def_default_handler	EXTI15_10_IRQHandler
	def_default_handler	RTC_Alarm_IRQHandler
	def_default_handler	USBWakeUp_IRQHandler
	def_default_handler	TIM8_BRK_IRQHandler
	def_default_handler	TIM8_UP_IRQHandler
	def_default_handler	TIM8_TRG_COM_IRQHandler
	def_default_handler	TIM8_CC_IRQHandler
	def_default_handler	ADC3_IRQHandler
	def_default_handler	SPI3_IRQHandler
	def_default_handler	UART4_IRQHandler
	def_default_handler	UART5_IRQHandler
	def_default_handler	TIM6_DAC_IRQHandler
	def_default_handler	TIM7_IRQHandler
	def_default_handler	DMA2_Channel1_IRQHandler
	def_default_handler	DMA2_Channel2_IRQHandler
	def_default_handler	DMA2_Channel3_IRQHandler
	def_default_handler	DMA2_Channel4_IRQHandler
	def_default_handler	DMA2_Channel5_IRQHandler
	def_default_handler	ADC4_IRQHandler
	def_default_handler	COMP1_2_3_IRQHandler
	def_default_handler	COMP4_5_6_IRQHandler
	def_default_handler	COMP7_IRQHandler
	def_default_handler	USB_HP_IRQHandler
	def_default_handler	USB_LP_IRQHandler
	def_default_handler	USBWakeUp_RMP_IRQHandler
	def_default_handler	FPU_IRQHandler
	
    def_default_handler    Default_Handler

    .weak    DEF_IRQHandler
    .set    DEF_IRQHandler, Default_Handler

    .end
