/*
*********************************************************************************************************
*                                              EXAMPLE CODE
*
*                             (c) Copyright 2011; Micrium, Inc.; Weston, FL
*
*                   All rights reserved.  Protected by international copyright laws.
*                   Knowledge of the source code may not be used to write a similar
*                   product.  This file may only be used in accordance with a license
*                   and should not be redistributed in any way.
*********************************************************************************************************
*/

/*
*********************************************************************************************************
*
*                                      APPLICATION CONFIGURATION
*
*                                     ST Microelectronics STM32
*                                              on the
*
*                                           STM3240G-EVAL
*                                         Evaluation Board
*
* Filename      : app_cfg.h
* Version       : V1.00
* Programmer(s) : FT
*                 DC
*********************************************************************************************************
*/

#ifndef  APP_CFG_MODULE_PRESENT
#define  APP_CFG_MODULE_PRESENT

/*
*********************************************************************************************************
*                                       MODULE ENABLE / DISABLE
*********************************************************************************************************
*/

#define  APP_CFG_SERIAL_EN                      DEF_ENABLED

/*
*********************************************************************************************************
*                                            TASK PRIORITIES
*********************************************************************************************************
*/
#define  APP_CFG_TASK_START_PRIO                          2u

#define  OS_TASK_TMR_PRIO                        (OS_LOWEST_PRIO - 2u)

/*
*********************************************************************************************************
*                                            TASK STACK SIZES
*                             Size of the task stacks (# of OS_STK entries)
*********************************************************************************************************
*/

#define  APP_CFG_TASK_START_STK_SIZE                    256u


/*
*********************************************************************************************************
*                                                 uC/SERIAL
*
* Note(s) : (1) Configure SERIAL_CFG_MAX_NBR_IF to the number of interfaces (i.e., UARTs) that will be
*               present.
*
*           (2) Configure SERIAL_CFG_RD_BUF_EN to enable/disable read buffer functionality.  The serial
*               core stores received data in the read buffer until the user requests it, providing a
*               reliable guarantee against receive overrun.
*
*           (3) Configure SERIAL_CFG_WR_BUF_EN to enable/disable write buffer functionality.  The serial
*               core stores line driver transmit data in the write buffer while the serial interface is
*               transmitting application data.
*
*           (4) Configure SERIAL_CFG_ARG_CHK_EXT_EN to enable/disable extended argument checking
*               functionality.
*
*           (5) Configure SERIAL_CFG_TX_DESC_NBR to allow multiple transmit operations (i.e., Serial_Wr,
*               Serial_WrAsync) to be queued.
*********************************************************************************************************
*/

#define  SERIAL_CFG_MAX_NBR_IF                            2u    /* See Note #1.                                         */

#define  SERIAL_CFG_RD_BUF_EN                    DEF_ENABLED    /* See Note #2.                                         */

#define  SERIAL_CFG_WR_BUF_EN                    DEF_ENABLED    /* See Note #3.                                         */

#define  SERIAL_CFG_ARG_CHK_EXT_EN               DEF_DISABLED   /* See Note #4.                                         */

#define  SERIAL_CFG_TX_DESC_NBR                            1    /* See Note #5.                                         */

/*
*********************************************************************************************************
*                                    uC/SERIAL APPLICATION CONFIGURATION
*********************************************************************************************************
*/

#define  APP_SERIAL_CFG_TRACE_EN                DEF_ENABLED
#define  APP_SERIAL_CFG_TRACE_PORT_NAME         "USART3"


/*
*********************************************************************************************************
*                                     TRACE / DEBUG CONFIGURATION
*********************************************************************************************************
*/
#if 0
#define  TRACE_LEVEL_OFF                               0
#define  TRACE_LEVEL_INFO                              1
#define  TRACE_LEVEL_DBG                               2
#endif

#include <cpu.h>
void  App_SerPrintf  (CPU_CHAR *format, ...);

#define  APP_TRACE_LEVEL                        TRACE_LEVEL_DBG
#define  APP_TRACE                              App_SerPrintf

#define  APP_TRACE_INFO(x)               ((APP_TRACE_LEVEL >= TRACE_LEVEL_INFO)  ? (void)(APP_TRACE x) : (void)0)
#define  APP_TRACE_DBG(x)                ((APP_TRACE_LEVEL >= TRACE_LEVEL_DBG)   ? (void)(APP_TRACE x) : (void)0)

#endif
