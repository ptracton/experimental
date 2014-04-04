/*
 * main.c
 *
 *  Created on: Apr 3, 2014
 *      Author: ptracton
 */
//
// http://stackoverflow.com/questions/19395898/microblaze-mcs-fixed-timer-interrupts
//
#include <mb_interface.h>
#include <xil_types.h>
typedef struct{
	u32 REG0;
	u32 REG1;
	u32 REG2;
	u32 REG3;
} MB_IO_SLAVE_TypeDef;
#define GPO1_BASE        (0x80000010)
#define GPI1_BASE        (0x80000020)
#define MB_IO_SLAVE_BASE (0xC0001000)

#define MB_IO_SLAVE ((MB_IO_SLAVE_TypeDef *) (MB_IO_SLAVE_BASE))
#define GPI1        ((u32 *) (GPI1_BASE))
#define GPO1        ((u32 *) (GPO1_BASE))

#include <xparameters.h>
#include <xiomodule.h>
#include <xiomodule_l.h>

XIOModule gpo1;
volatile u32 ct = 0;

void timerTick(void* ref) {
    ct++;
    XIOModule_DiscreteWrite(&gpo1, 1, ct);
    XIOModule_DiscreteWrite(&gpo1, 2, ct);
}

int main() {

    XIOModule_Initialize(&gpo1, XPAR_IOMODULE_0_DEVICE_ID);

    microblaze_register_handler(XIOModule_DeviceInterruptHandler, XPAR_IOMODULE_0_DEVICE_ID);

    XIOModule_Start(&gpo1);

    XIOModule_Connect(&gpo1, XIN_IOMODULE_FIT_1_INTERRUPT_INTR, timerTick, NULL);
    XIOModule_Enable(&gpo1,XIN_IOMODULE_FIT_1_INTERRUPT_INTR);

    microblaze_enable_interrupts();
    while (1) {
    }
}
