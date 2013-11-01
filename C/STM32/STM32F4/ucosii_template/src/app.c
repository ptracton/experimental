
#include <stm32f4xx_conf.h>
#include "includes.h"
#include "task1.h"

//
// Mutexes for shared HW
//
OS_EVENT * USART2_Mutex;

void APP_CreateTasks(void)
{
    INT8U retval;
    
    
    retval = OSTaskCreate(&Task1_Task,      (void *) 0,             &task1_stack[TASK1_STACK_SIZE-1],     23);
    if (retval != OS_ERR_NONE){
	while(1);
    }
    OSTaskNameSet(23, "TASK1", &retval);
    

    return;    
}

void APP_CreateMBoxes(void)
{

    task1_mbox = OSMboxCreate((TASK1_MBOX_TypeDef *)0);
    return;    
}

void APP_CreateMutexes(void)
{
    INT8U err;
    INT8U prio = 2;
    
    USART2_Mutex = OSMutexCreate(prio, &err);
    while (err != OS_ERR_NONE){
	USART2_Mutex = OSMutexCreate(prio,&err);
    }

    return;    
}

void APP_GetMutex(OS_EVENT * mutex)
{
    INT8U err;
       
    OSMutexPend(mutex, 0, &err);
    while (err != OS_ERR_NONE){
	OSMutexPend(mutex, 0, &err);
    }

    return;    
}

void APP_ReleaseMutex(OS_EVENT * mutex)
{
    INT8U retval;
    
    retval = OSMutexPost(mutex);
    while (retval != OS_ERR_NONE){
	retval = OSMutexPost(mutex);
    }
    return;    
}
