

#ifndef INC_FREERTOS_CONFIG_H
#define INC_FREERTOS_CONFIG_H

#define configUSE_PREEMPTION  1
#define configUSE_IDLE_HOOK   0
#define configUSE_TICK_HOOK   0
#define configUSE_CO_ROUTINES 0
#define INCLUDE_vTaskPrioritySet 0
#define INCLUDE_uxTaskPriorityGet 0
#define INCLUDE_vTaskDelete 0
#define INCLUDE_vTaskSuspend 0
#define INCLUDE_vTaskDelayUntil 0
#define INCLUDE_vTaskDelay 0
#define configUSE_16_BIT_TICKS 0


#define configMAX_CO_ROUTINE_PRIORITIES 1
#define configMAX_PRIORITIES 4
#define configMINIMAL_STACK_SIZE 32
#define configKERNEL_INTERRUPT_PRIORITY 0
#define onfigMAX_SYSCALL_INTERRUPT_PRIORITY 0
#define configMAX_SYSCALL_INTERRUPT_PRIORITY 0
#define configCPU_CLOCK_HZ (168000000uL)
#define configTICK_RATE_HZ 100

#define configTOTAL_HEAP_SIZE 128

#endif

