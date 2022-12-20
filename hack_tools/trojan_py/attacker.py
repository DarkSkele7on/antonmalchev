import socket

class Attacker:
    def __init__(self):
        # Create a socket object
        self.sock = socket.socket()

        # Get the local machine name
        self.host = socket.gethostname()

        # Set the port number
        self.port = 12345

    def connect(self):
        # Connect to the server
        self.sock.connect((self.host, self.port))

    def send_message(self, message):
        # Convert the message to a bytes-like object
        message = message.encode()

        # Send the message to the server
        self.sock.send(message)

    def close(self):
        # Close the connection
        self.sock.close()

if __name__ == "__main__":
    # Create a client object
    attacker = Attacker()
    
    # Connect to the server
    attacker.connect()

    # Send a message to the server
    attacker.send_message("Hello, server!")

    # Close the connection
    attacker.close()

