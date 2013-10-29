#include <stm32f4xx.h>
#include <FreeRTOS.h>
#include <task.h>

int main(void)
{
    

    vTaskStartScheduler();
    return 0;    
}
