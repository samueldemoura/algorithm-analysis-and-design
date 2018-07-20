TARGET  := bin/algorithms
SRCDIR  := src
INCDIR  := include
SRC     := $(shell find $(SRCDIR) -name "*.cpp" -type f)
OBJDIR  := obj
OBJ     := $(SRC:%.cpp=$(OBJDIR)/%.o)

CC      := g++
CFLAGS  := -I$(SRCDIR) -I$(INCDIR) -Wall -Wextra -O2 -std=c++11
LDFLAGS :=
#DFLAG   := -DDEBUG

$(TARGET): $(OBJ)
	@mkdir -p bin
	@echo "\033[1;33m=> Linking\033[0m $@"
	@$(CC) $(LDFLAGS) -o $@ $^
	@echo "\033[1;32m=> Done!\033[0m"

$(OBJDIR)/%.o: %.cpp
	@echo "\033[1;33m=> Compiling\033[0m $<"
	@mkdir -p $(shell dirname $@)
	@$(CC) $(CFLAGS) $(DFLAG) -c $< -o $@

clean:
	@echo "\033[1;33m=> Removing\033[0m $(OBJDIR)"
	-@rm -r $(OBJDIR)

mrproper: clean
	@echo "\033[1;33m=> Removing\033[0m $(TARGET)"
	-@rm $(TARGET)

all: mrproper $(TARGET)
