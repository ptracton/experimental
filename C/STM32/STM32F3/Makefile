
DIRS = STM32F30x_StdPeriph_Driver
DIRS += freertos_template
DIRS += freertos_cli_template
DIRS += stm32f3_basic
DIRS += template
DIRS += timer
DIRS += uart_echo
DIRS += ucosii_template

all:
	$(foreach c,$(DIRS),$(MAKE) -C $(c) && ) true

clean:
	rm -f *~
	$(foreach c,$(DIRS),$(MAKE) -C $(c) clean && ) true