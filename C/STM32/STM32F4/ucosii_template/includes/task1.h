
#ifndef __TASK1_H__
#define __TASK1_H__

#define TASK1_STACK_SIZE 128
#define OS_MBOX_TIMEOUT_MAX (0xFFFF)
   
extern OS_STK   task1_stack[TASK1_STACK_SIZE]; 
extern OS_EVENT *task1_mbox;

typedef struct
{
    INT8U action;    
} TASK1_MBOX_TypeDef;

    

void Task1_Task(void *);

#endif
