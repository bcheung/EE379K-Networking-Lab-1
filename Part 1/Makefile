CC = gcc
CFLAGS = -I.
DEPS = constants.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

build: build-client build-server

build-client: client.o
	$(CC) -o client client.o $(CFLAGS)

build-server: server.o
	$(CC) -o server server.o $(CFLAGS)
