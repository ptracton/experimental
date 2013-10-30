
#ifndef __TASK2_H__
#define __TASK2_H__

#define Task2_STACK_SIZE 32
#define Task2_QUEUE_SIZE 4

extern xQueueHandle xTask2_Queue;

typedef struct
{
    uint8_t action;
    uint32_t ptr;
} xTask2_Message;


void Task2_Task( void *pvParameters );

#endif
