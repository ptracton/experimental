#include <stm32l1xx.h>
#include <FreeRTOS.h>
#include <task.h>

int main(void)
{
    

    vTaskStartScheduler();
    return 0;    
}
