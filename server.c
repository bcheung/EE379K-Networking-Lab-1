#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h> 
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include <constants.h>

void str_to_upper(char str[]) {
    int i = 0;
    while(str[i]) {
        str[i] = toupper(str[i]);
        i++;
    }
}

int main() {

    char buf[100];

    // file descriptors for reading and writing to socket
    int server_fd, client_fd;
    char *client_ip;
 
    // struct to store server IP address and port numbers of server and client
    struct sockaddr_in serv_addr;
    struct sockaddr_in client_addr;

    int addr_len = sizeof(client_addr); 

    // listen for connections by creating socket
    // socket(domain=IPv4 protocol, type of socket=TCP, protocol)
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("ERROR creating socket"); 
        exit(EXIT_FAILURE);
    }
 
    // clear serv_addr
    bzero(&serv_addr, sizeof(serv_addr));
 
    // set addressing scheme to IPv4
    serv_addr.sin_family = AF_INET;

    // allow any IP to connect
    // htons() converts to big-endian format (most significant byte first)
    serv_addr.sin_addr.s_addr = htons(INADDR_ANY);

    // listen to SERVER_PORT = 12000
    serv_addr.sin_port = htons(SERVER_PORT);
 
    // binds the address/port specified by serv_addr to the socket server_fd (assign name to socket)
    bind(server_fd, (struct sockaddr *) &serv_addr, sizeof(serv_addr));
 
    // start listening for connections, keep at most 5 connections
    if (listen(server_fd, 5) < 0) {
        perror("ERROR on listen"); 
        exit(EXIT_FAILURE); 
    }
 
    printf("The server is ready to receive\n");

    
    while(1) {
 
        // accept a connection from any client willing to connect, wait if no client willing to connect
        // file descriptor to read/write to client is returned
        if ((client_fd = accept(server_fd, (struct sockaddr *) &client_addr, (socklen_t*) &addr_len)) < 0) { 
            perror("ERROR on accept"); 
            exit(EXIT_FAILURE); 
        }

        // convert IPv4 and IPv6 addresses from binary form to string
        client_ip = inet_ntoa(client_addr.sin_addr);

        printf("Client connected\nIP Address: %s:%d\n", client_ip, client_addr.sin_port);
        // print(addr)
        // print(connectionSocket, addr)

        // clear buf buffer
        bzero(buf, 100);

        // read from client and store into buf
        if (read(client_fd, buf, 100) < 0) { 
            perror("ERROR reading from socket"); 
            exit(EXIT_FAILURE); 
        }
        
        printf("From client: %s\n", buf);

        str_to_upper(buf);        

        printf("To client: %s\n", buf);


        // write buf to client (strlen(buf) + 1 includes length of actual string + null character)
        if (write(client_fd, buf, strlen(buf) + 1) < 0) { 
            perror("ERROR writing to socket"); 
            exit(EXIT_FAILURE); 
        }
  
        shutdown(client_fd, SHUT_RDWR);

        // close client socket connection
        close(client_fd);
    }
}
