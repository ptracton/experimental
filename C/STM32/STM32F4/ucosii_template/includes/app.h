
#ifndef __APP_H__
#define __APP_H__

extern OS_EVENT * USART2_Mutex;

void APP_CreateTasks(void);
void APP_CreateMBoxes(void);
void APP_CreateMutexes(void);
void APP_GetMutex(OS_EVENT * mutex);
void APP_ReleaseMutex(OS_EVENT * mutex);

#endif
