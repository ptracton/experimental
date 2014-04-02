/*
 * simple_application.h
 *
 *  Created on: Apr 1, 2014
 *      Author: tractp1
 */

#ifndef SIMPLE_APPLICATION_H_
#define SIMPLE_APPLICATION_H_

#include <xil_types.h>
#include "mb_io_slave.h"


#define GPO1_BASE        (0x80000010)
#define GPI1_BASE        (0x80000020)
#define MB_IO_SLAVE_BASE (0xC0001000)

#define MB_IO_SLAVE ((MB_IO_SLAVE_TypeDef *) (MB_IO_SLAVE_BASE))
#define GPI1        ((u32 *) (GPI1_BASE))
#define GPO1        ((u32 *) (GPO1_BASE))

#endif /* SIMPLE_APPLICATION_H_ */
