
##
## Name of our project and executable
##
TARGET = main

SRC_DIR = src
OBJ_DIR = objects
INC_DIR = includes
EXEC_DIR = executable

SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS  = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

ELF_FILE  = $(EXEC_DIR)/$(TARGET).elf
LIST_FILE = $(EXEC_DIR)/$(TARGET).lst
HEX_FILE  = $(EXEC_DIR)/$(TARGET).hex
SREC_FILE = $(EXEC_DIR)/$(TARGET).srec
BIN_FILE  = $(EXEC_DIR)/$(TARGET).bin

#TOOLCHAIN_DIR = /home/ptracton/src/software/STM32/libopencm3
TOOLCHAIN_DIR = $(LIBOPENCM3_PATH)
LDSCRIPT = src/stm32f3-discovery.ld

PREFIX	?= arm-none-eabi
# PREFIX		?= arm-elf
CC		= $(PREFIX)-gcc
LD		= $(PREFIX)-gcc
OBJCOPY		= $(PREFIX)-objcopy
OBJDUMP		= $(PREFIX)-objdump
GDB		= $(PREFIX)-gdb
FLASH		= $(shell which st-flash)

OOCD		?= openocd
OOCD_INTERFACE	?= stlink-v2
OOCD_BOARD	?= stm32f3discovery


CFLAGS		+= -Os -g -Wall -Wextra -I$(TOOLCHAIN_DIR)/include \
		   -fno-common -mcpu=cortex-m4 -mthumb \
		   -mfloat-abi=hard -mfpu=fpv4-sp-d16 -MD -DSTM32F3

#LDFLAGS		+= --static -lc -lnosys -L$(TOOLCHAIN_DIR)/lib \
			 -L$(TOOLCHAIN_DIR)/lib/stm32/f3 \
		   -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections \
		   -mthumb -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16

LDFLAGS		+= --static -lc -L$(TOOLCHAIN_DIR)/lib \
			 -L$(TOOLCHAIN_DIR)/lib/stm32/f3 \
		   -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections \
		   -mthumb -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16

all: $(LIST_FILE) $(HEX_FILE) $(SREC_FILE) $(BIN_FILE)

$(HEX_FILE) :$(ELF_FILE)
	$(OBJCOPY) -Oihex $(ELF_FILE) $(HEX_FILE)

$(SREC_FILE):$(ELF_FILE)
	$(OBJCOPY) -Osrec $(ELF_FILE)  $(SREC_FILE)

$(BIN_FILE):$(ELF_FILE)
	$(OBJCOPY) -Obinary $(ELF_FILE) $(BIN_FILE)

$(LIST_FILE):$(ELF_FILE)
	$(OBJDUMP) -S $(ELF_FILE) >  $(LIST_FILE)

$(ELF_FILE): $(OBJECTS)
	$(LD) -o $(ELF_FILE) $(OBJECTS) -lopencm3_stm32f3 $(LDFLAGS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c 
	@echo $@ $<  
	$(CC) $(CFLAGS) -o $@ -c $< 


FLASH: $(BIN_FILE)
	$(FLASH) write $(BIN_FILE) 0x8000000

clean:
	rm -f $(OBJECTS) $(SRC_DIR)/*~ *~ $(ELF_FILE) $(LIST_FILE) $(BIN_FILE) $(HEX_FILE) $(SREC_FILE) $(OBJ_DIR)/*.d

.PHONY: images clean

-include $(OBJS:.o=.d)

