#include <stm32f4xx_conf.h>
#include "includes.h"


int main(void)
{
    //
    // BSP -- Board Support Package, set up the HW
    //
    BSP_Init();
    
    //
    // Call before doing any OS operations
    //
    OSInit();
    
    //
    // Create the resource protecting mutexes
    //
    APP_CreateMutexes();    

    //
    // Create the message passing mail boxes
    //
    APP_CreateMBoxes();
    
    //
    // Create the tasks 
    //
    APP_CreateTasks();
        
    //
    // Start the OS, we do NOT return from here unless something has gone really wrong
    //
    OSStart(); 
    
    return 0;    
}
