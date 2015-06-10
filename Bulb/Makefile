CC = gcc
SRCS = lightbulb.c
OBJS = $(SRCS:.c=.o)
INCLUDES =
LIBDIRS =
LIBS = -lparse -pthread
TARGET = lightbulb 

all: $(TARGET)

$(TARGET): $(OBJS) 
	$(CC) $(LIBDIRS) $(OBJS) -o $(TARGET) $(LIBS)

.c.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -fR $(TARGET) $(OBJS)

