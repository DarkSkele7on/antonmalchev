#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>

#define PORT 4444

int sock_fd;
struct sockaddr_in serv_addr;

void createSocket() {
    // Create a socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        fprintf(stderr, "Error creating socket\n");
        exit(1);
    }
}

void connectToServer(char* ip) {
    // Set up the server address
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, ip, &serv_addr.sin_addr) <= 0) {
        fprintf(stderr, "Error setting up server address\n");
        exit(1);
    }

    // Connect to the server
    if (connect(sock_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        fprintf(stderr, "Error connecting to server\n");
        exit(1);
    }
}

void sendCommand(char* command) {
    // Send a command or script name to the server
    if (send(sock_fd, command, strlen(command), 0) < 0) {
        fprintf(stderr, "Error sending data\n");
        exit(1);
    }
}

void receiveResponse(char* buffer, int buffer_size) {
    // Receive the response from the server
    int bytes_received = recv(sock_fd, buffer, buffer_size, 0);
    if (bytes_received < 0) {
        fprintf(stderr, "Error receiving data\n");
        exit(1);
    }
}

void closeSocket() {
    // Close the socket
    close(sock_fd);
}

int main(int argc, char *argv[]) {
    char buffer[1024];

    createSocket();
    connectToServer("192.168.2.163");
    sendCommand("ls");
    //receiveResponse(buffer, sizeof(buffer));
    //printf("%.*s\n", strlen(buffer), buffer);
    //closeSocket();

    return 0;
}
