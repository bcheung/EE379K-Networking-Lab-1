#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h> 
#include <stdio.h>
#include <string.h>

#include <constants.h>

int main() {

    int sock_fd, n;
    char write_buf[100];
    char read_buf[100];

    struct sockaddr_in servaddr;
 
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    bzero(&servaddr, sizeof servaddr);
 
    servaddr.sin_family=AF_INET;
    servaddr.sin_port=htons(SERVER_PORT);
 
    // convert IPv4 and IPv6 addresses from text to binary form and store into servaddr.sin_addr
    inet_pton(AF_INET, SERVER_IP, &(servaddr.sin_addr));
 
    // connect to server with address and port number specified in servaddr.
    if(connect(sock_fd, (struct sockaddr *) &servaddr, sizeof(servaddr)) < 0) {
        perror("ERROR connecting to server"); 
        exit(EXIT_FAILURE); 
    };

    printf("Connected to server\n");
    printf("Input lowercase sentence:\n");

    // stdin = 0 , for standard input
    // read string from stdin and store in write_buf
    // reads new line character
    fgets(write_buf, 100, stdin);

    // write write_buf to socket
    write(sock_fd, write_buf, strlen(write_buf) + 1);

    // read from server and store into read_buf
    read(sock_fd, read_buf, 100);

    printf("From Server: %s\n", read_buf);

    close(sock_fd);
}