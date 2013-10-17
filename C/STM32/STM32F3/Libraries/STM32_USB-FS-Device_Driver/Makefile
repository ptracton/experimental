
##
## This is the library we are making
##
TARGET = stm32usb

##
## Tool Set defaults to arm-none-eabi
##
PREFIX	?= arm-none-eabi
CC	= $(PREFIX)-gcc
LD	= $(PREFIX)-gcc
OBJCOPY	= $(PREFIX)-objcopy
OBJDUMP	= $(PREFIX)-objdump
GDB	= $(PREFIX)-gdb
AR	= $(PREFIX)-ar

##
## Directory structure
##

SRC_DIR = src
OBJ_DIR = objects
INC_DIR = inc
LIB_DIR = lib

##
## Output files we will produce
##
LIB_FILE  = $(LIB_DIR)/lib$(TARGET).a

##
## SOURCE are just all of the C files in the SRC_DIR.  For each .C 
## there will be a .o
##
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS  = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

STD_PERIPHERAL_INCLUDE = ../../Libraries/STM32F30x_StdPeriph_Driver/inc/

##
## Compiler flags
##
CFLAGS	+= -Os -g -Wall -Wextra -I $(INC_DIR) -I$(STD_PERIPHERAL_INCLUDE)\
	-I ../CMSIS/Device/ST/STM32F30x/Include/\
	-I ../CMSIS/Include -I../../Project/Demonstration/\
	   -fno-common -mcpu=cortex-m4 -mthumb \
	   -mfloat-abi=hard -mfpu=fpv4-sp-d16 -MD -DSTM32F3 -DSTM32F30X -DUSE_STDPERIPH_DRIVER
##
## Build everything
##
all: dirs $(LIB_FILE)

##
## Create the directories we will need
##
dirs:
	@echo "Making Directories"
	@mkdir -p $(OBJ_DIR)
	@mkdir -p $(LIB_DIR)

##
## Build the library file, but it depends on the OBJECTS
##
$(LIB_FILE): $(OBJECTS)
	@echo "Building $(LIB_FILE)"
	$(AR) rcs $(LIB_FILE) $(OBJECTS)
##
## Build the objects which depend on the C files
##
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c 
	@echo "Building $<"
	@$(CC) $(CFLAGS) -o $@ -c $< 


clean:
	find ./ -name '*~' | xargs rm -f     	
	rm -rf $(LIB_DIR) $(OBJ_DIR)

##
## Create depdendency files
##
-include $(OBJS:.o=.d)

