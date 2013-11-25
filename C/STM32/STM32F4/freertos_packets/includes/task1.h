
#ifndef __TASK1_H__
#define __TASK1_H__

#define Task1_STACK_SIZE 256
#define Task1_QUEUE_SIZE 4

extern xQueueHandle xTask1_Queue;

typedef struct
{
    uint16_t character;
    uint32_t ptr;
} xTask1_Message;

    

void Task1_Task( void *pvParameters );

#endif
