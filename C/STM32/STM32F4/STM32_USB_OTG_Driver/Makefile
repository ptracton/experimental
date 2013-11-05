
##
## This is the library we are making
##
TARGET = libstm32f4xx_usbotg.a
CINCLUDES += -I../STM32F4xx_StdPeriph_Driver/inc/
CFLAGS += -DUSB_OTG_HS_CORE
CFLAGS += -DUSE_USB_OTG_HS
CFLAGS += -DUSE_EMBEDDED_PHY
TARGET_DIR = lib
LIBRARY = 1
COMMON_DIR = ../common
COMMON_INC = $(COMMON_DIR)/includes
CINCLUDES += -I$(COMMON_INC)

include ../Makefile.stm32f4

