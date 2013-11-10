
#ifndef __CLI_TASK_H__
#define __CLI_TASK_H__

#define CLI_STACK_SIZE 256
#define CLI_TASK_QUEUE_SIZE 4

extern xQueueHandle xCLI_Queue;

typedef struct
{
    uint16_t character;    
} xCLI_Message;

void vCLI_Task(void * pvParameters);
    

#endif

