
#include <stm32f4xx_conf.h>
#include "includes.h"

//
// Mutexes for shared HW
//
OS_EVENT * USART2_Mutex;

void APP_CreateTasks(void)
{
    return;    
}

void APP_CreateMBoxes(void)
{
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
