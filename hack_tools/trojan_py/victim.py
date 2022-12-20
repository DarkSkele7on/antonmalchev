import socket

class Victim:
    def __init__(self):
        # Create a socket object
        self.sock = socket.socket()

        # Get the local machine name
        self.host = socket.gethostname()

        # Set the port number
        self.port = 12345

        # Bind the socket to the host and port
        self.sock.bind((self.host, self.port))

    def listen(self):
        # Start listening for incoming connections
        self.sock.listen(5)

    def accept_connection(self):
        # Accept an incoming connection
        self.conn, self.addr = self.sock.accept()

        # Print the address of the client
        print("Connected by", self.addr)

    def receive_data(self):
        # Receive data from the client
        self.data = self.conn.recv(1024)

        # Print the received data
        print("Received:", self.data)

    def send_response(self, message):
        # Send a response to the client
        self.conn.send(message)

    def close_connection(self):
        # Close the connection
        self.conn.close()

if __name__ == "__main__":
    # Create a server object
    server = Victim()

    # Start listening for incoming connections
    server.listen()

    # Accept an incoming connection
    server.accept_connection()

    # Receive data from the client
    server.receive_data()

    # Send a response to the client
    server.send_response("Thank you for connecting!")

    # Close the connection
    server.close_connection()
