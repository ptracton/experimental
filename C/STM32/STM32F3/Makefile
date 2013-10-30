
DIRS = STM32F30x_StdPeriph_Driver
DIRS += freertos_template
DIRS += stm32f3_basic
DIRS += template
DIRS += timer
DIRS += uart_echo

all:
	$(foreach c,$(DIRS),$(MAKE) -C $(c) && ) true

clean:
	rm -f *~
	$(foreach c,$(DIRS),$(MAKE) -C $(c) clean && ) true