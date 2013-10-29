
##
## Tools to use
##
CC		= gcc
LD		= gcc
OBJCOPY		= objcopy
OBJDUMP		= objdump
GDB		= gdb
AR              = ar
RM              = rm
MKDIR           = mkdir

##
## Our basic directory structure
##
SRC_DIR = src
OBJ_DIR = objects
INC_DIR = includes

##
## Commonly used includes
##
LIB1_INC = ../lib1/includes
LIB2_INC = ../lib2/includes

##
## Library 1 link details
##
LIB1_LIB_DIR = ../lib1/lib
LIB1_LIBRARY = lib1

##
## Library 2 link details
##
LIB2_LIB_DIR = ../lib2/lib
LIB2_LIBRARY = lib2

##
## Parameters for linking, this allows a sub makefile to add more here
##
LINK_LIB_PATHS += -L$(LIB1_LIB_DIR)  -L$(LIB2_LIB_DIR) 
LINK_LIBRARIES += -l$(LIB1_LIBRARY)  -l$(LIB2_LIBRARY) 

##
## Our include paths.  Sub makefiles can add more
##
CINCLUDES += -I$(LIB1_INC)
CINCLUDES += -I$(LIB2_INC)
CINCLUDES += -Iincludes

##
## Our C compiler flags, sub make files can add more
##
CFLAGS += -Os -g -Wall -Wextra $(CINCLUDES)

##
## The source list turned into an object list for this build
##
SOURCES  += $(wildcard $(SRC_DIR)/*.c)
OBJECTS  += $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

##
## The directories to make for this build.
##
MAKE_DIRS += $(OBJ_DIR) $(TARGET_DIR)

##
## These are other directories that must be build for this application
##
BUILD_DIRS += ../lib1 
BUILD_DIRS += ../lib2 

##
## If we are not building a library, include the common C and H files
##
ifeq ($(LIBRARY),0)
COMMON_DIR = ../common
COMMON_SRC_DIR = $(COMMON_DIR)/$(SRC_DIR)
COMMON_INC_DIR = $(COMMON_DIR)/$(INC_DIR)

##
## Look in the $(COMMON_INC_DIR) for header files
##
CINCLUDES += -I$(COMMON_INC_DIR)

##
## Get our list of common source code and turn it into a list of objects
##
COMMON_SOURCES  += $(wildcard $(COMMON_SRC_DIR)/*.c)
COMMON_OBJECTS  += $(patsubst $(COMMON_SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(COMMON_SOURCES))

##
## Add the common objects to the list of objects need for our $(TARGET) so that they get built
##
OBJECTS += $(COMMON_OBJECTS)

##
## Look in $(COMMON_SRC_DIR) for code to build
##
VPATH += $(COMMON_SRC_DIR)

endif

##
## This is our target to build.  The submakefile is responsible for spelling out 
## $(TARGET_DIR) and $(TARGET)
##
EXECUTABLE = $(TARGET_DIR)/$(TARGET)

##
## Look in $(SRC_DIR) for code to build
##
VPATH += $(SRC_DIR)

##
## This is our build process entry point.  We need to make our directories to store our 
## objects and final target
##
all:dirs $(EXECUTABLE)

##
## For each of the directories in $(MAKE_DIRS) create it
##
dirs:
	@echo "Making directories $(MAKE_DIRS)"
	@$(MKDIR) -p $(MAKE_DIRS)


$(EXECUTABLE):$(OBJECTS)
ifeq ($(LIBRARY),1)
	@echo "Building Library $(TARGET_DIR)/$(TARGET)"
	@$(AR) rcs $(TARGET_DIR)/$(TARGET) $(OBJECTS)
else
	@echo "Build Libraries"
	$(foreach c,$(BUILD_DIRS),$(MAKE) -C $(c) && ) true

	@echo "Building Executable $(TARGET_DIR)/$(TARGET)"
	$(LD) $(OBJECTS) $(LINK_LIB_PATHS) $(LINK_LIBRARIES) -o $(TARGET_DIR)/$(TARGET)
endif

##
## Turn out C code into objects in our $(OBJ_DIR)
##
$(OBJ_DIR)/%.o:%.c
	@echo "Building Object $@"
	@$(CC) $(CFLAGS) -o $@ -c $< 

.PHONY: clean

##
## Clean this local part of the project
##
clean:
	$(RM) -rf $(MAKE_DIRS)
	$(RM) -f  $(SRC_DIR)/*~
	$(RM) -f  $(INC_DIR)/*~
	$(RM) -f  *~

##
## Clean everything
##
all_clean: clean
	$(RM) -f ../common/$(SRC_DIR)/*~
	$(RM) -f ../common/$(INC_DIR)/*~
	$(foreach c,$(BUILD_DIRS),$(MAKE) -C $(c) clean && ) true

-include $(OBJECTS:.o=.d)

