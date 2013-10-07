
TOOLCHAIN_DIR = /home/ptracton/src/software/STM32/libopencm3

BINARY = main
LDSCRIPT = src/stm32f3-discovery.ld

PREFIX	?= arm-none-eabi
# PREFIX		?= arm-elf
CC		= $(PREFIX)-gcc
LD		= $(PREFIX)-gcc
OBJCOPY		= $(PREFIX)-objcopy
OBJDUMP		= $(PREFIX)-objdump
GDB		= $(PREFIX)-gdb
FLASH		= $(shell which st-flash)

CFLAGS		+= -Os -g -Wall -Wextra -I$(TOOLCHAIN_DIR)/include \
		   -fno-common -mcpu=cortex-m4 -mthumb \
		   -mfloat-abi=hard -mfpu=fpv4-sp-d16 -MD -DSTM32F3
LDFLAGS		+= --static -lc -lnosys -L$(TOOLCHAIN_DIR)/lib \
			 -L$(TOOLCHAIN_DIR)/lib/stm32/f3 \
		   -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections \
		   -mthumb -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16
OBJS		+= objects/$(BINARY).o

OOCD		?= openocd
OOCD_INTERFACE	?= stlink-v2
OOCD_BOARD	?= stm32f3discovery

all: $(BINARY).elf $(BINARY).bin $(BINARY).hex $(BINARY).srec $(BINARY).list

$(BINARY).images: %.bin %.hex %.srec %.list
	echo "*** $* images generated ***"

$(BINARY).bin: $(BINARY).elf
	$(OBJCOPY) -Obinary executable/$(BINARY).elf  executable/$(BINARY).bin

$(BINARY).hex: $(BINARY).elf
	$(OBJCOPY) -Oihex executable/$(BINARY).elf  executable/$(BINARY).hex

$(BINARY).srec: $(BINARY).elf
	$(OBJCOPY) -Osrec executable/$(BINARY).elf  executable/$(BINARY).srec

$(BINARY).list: $(BINARY).elf
	$(OBJDUMP) -S executable/$(BINARY).elf >  executable/$(BINARY).list

$(BINARY).elf: $(OBJS)
	$(LD) -o executable/$(BINARY).elf $(OBJS) -lopencm3_stm32f3 $(LDFLAGS)

$(OBJS):
	$(CC) $(CFLAGS) -o $@ -c src/main.c


$(BINARY).stlink-flash: $(BINARY).bin
	$(Q)$(FLASH) write executable/$(BINARY).bin 0x8000000

clean:
	/bin/rm -f objects/*.o src/*~ *~  executable/$(BINARY)*

.PHONY: images clean

-include $(OBJS:.o=.d)

