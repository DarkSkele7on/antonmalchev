#include <iostream>
#include <cstring>
#include <unistd.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 

#define PORT 8080

class Client {
private:
    int sock = 0;
    struct sockaddr_in serv_addr;

public:
    Client() {
        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
            std::cerr << "Socket creation error" << std::endl;
            exit(EXIT_FAILURE);
        }

        memset(&serv_addr, '0', sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(PORT);

        // Convert IPv4 and IPv6 addresses from text to binary form
        if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
            std::cerr << "Invalid address/ Address not supported" << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    int Connect() {
        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
            std::cerr << "Connection Failed" << std::endl;
            return -1;
        }

        return 0;
    }

    void Send(const std::string& message) {
        send(sock , message.c_str() , message.size() , 0 );
    }

    std::string Receive() {
        char buffer[1024] = {0};
        int valread = read(sock, buffer, 1024);
        return std::string(buffer, valread);
    }
};

int main() {
    Client client;
    if (client.Connect() < 0) {
        return -1;
    }

    client.Send("Hello from client");
    std::cout << "Message sent" << std::endl;
    std::cout << "Received: " << client.Receive() << std::endl;
    return 0;
}