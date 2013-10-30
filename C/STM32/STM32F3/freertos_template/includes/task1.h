
#ifndef __TASK1_H__
#define __TASK1_H__

#define Task1_STACK_SIZE 32
#define Task1_QUEUE_SIZE 4

extern xQueueHandle xTask1_Queue;

typedef struct
{
    uint8_t action;
    uint32_t ptr;
} xTask1_Message;

    

void Task1_Task( void *pvParameters );

#endif
