
DIRS = STM32F4xx_StdPeriph_Driver
DIRS += freertos_template
DIRS += ucosii_template
DIRS += stm32f4_basic
DIRS += timer
DIRS += template

all:
	$(foreach c,$(DIRS),$(MAKE) -C $(c) && ) true

clean:
	rm -f *~
	$(foreach c,$(DIRS),$(MAKE) -C $(c) clean && ) true
