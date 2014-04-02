/*
 * main.c
 *
 *  Created on: Apr 1, 2014
 *      Author: tractp1
 */

#include "simple_application.h"

int main(){

	MB_IO_SLAVE->REG0 = 0x12345678;
	MB_IO_SLAVE->REG1 = 0x9abcdef0;
	MB_IO_SLAVE->REG2 = 0x11223344;
	MB_IO_SLAVE->REG3 = 0x55667788;
	*GPO1 = MB_IO_SLAVE->REG0;
	while (*GPI1 != 0x12345678);
	*GPO1 = 0xdeadbeef;
	return 0;
}
