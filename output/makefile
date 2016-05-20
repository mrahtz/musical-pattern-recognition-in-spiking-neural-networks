PROGRAM = main
SRCS = objects.cpp main.cpp code_objects/neurongroup_stateupdater_codeobject.cpp code_objects/statemonitor_codeobject.cpp code_objects/spikemonitor_codeobject.cpp code_objects/neurongroup_thresholder_codeobject.cpp code_objects/neurongroup_resetter_codeobject.cpp network.cpp synapses_classes.cpp run.cpp
H_SRCS = objects.h code_objects/neurongroup_stateupdater_codeobject.h code_objects/statemonitor_codeobject.h code_objects/spikemonitor_codeobject.h code_objects/neurongroup_thresholder_codeobject.h code_objects/neurongroup_resetter_codeobject.h network.h synapses_classes.h run.h brianlib/common_math.h brianlib/clocks.h brianlib/dynamic_array.h
OBJS = ${SRCS:.cpp=.o}
CC = @g++
DEBUG = -g
OPTIMISATIONS = -w -O3 -ffast-math -march=native
CFLAGS = -c -Wno-write-strings $(OPTIMISATIONS) -I. 
LFLAGS =  
DEPS = make.deps

all: executable

# Adds debug flags
debug: CFLAGS += $(DEBUG)
debug: LFLAGS += $(DEBUG)
debug: executable

.PHONY: all debug executable clean

executable: $(OBJS) $(DEPS)
	$(CC) $(OBJS) -o $(PROGRAM) $(LFLAGS)

clean:
	rm $(OBJS) $(PROGRAM) $(DEPS)

make.deps: $(SRCS) $(H_SRCS)
	$(CC) $(CFLAGS) -MM $(SRCS) > make.deps
	
ifneq ($(wildcard $(DEPS)), )
include $(DEPS)
endif

%.o : %.cpp
	$(CC) $(CFLAGS) $< -o $@