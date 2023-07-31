import os
import shlex
import signal
import socket
import socketserver
import subprocess
import platform
import zlib

COMMANDS = {
    "exit": "Client requested to close the connection.",
    "upload": "Upload a file to the server.",
    "download": "Download a file from the server.",
    "delete": "Delete a file on the server.",
    "rename": "Rename a file on the server.",
    "move": "Move a file on the server.",
    "stat": "Get server statistics (type: 'cpu', 'memory', or 'disk').",
    "help": "Display available commands.",
    "shutdown": "Shut down the server.",
    "end": "Close the server program entirely.",
}

class MyTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.client_socket = self.request

    def handle(self):
        print("Connected by:", self.client_address)

        try:
            while True:
                data = self.request.recv(1024).decode().strip()
                if not data:
                    break

                print("Received command:", data)
                command_args = shlex.split(data.lower())
                command = command_args[0]

                if command in COMMANDS:
                    handler_method = getattr(self, f"handle_{command}")
                    handler_method(command_args)
                else:
                    self.execute_shell_command(data)

        except ConnectionError:
            print("Connection error occurred.")
        except Exception as e:
            print(f"Error: {e}")

    def execute_shell_command(self, command):
        try:
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = process.stdout.strip() + process.stderr.strip()
            self.request.sendall(output.encode())
        except Exception as e:
            self.request.sendall(str(e).encode())

    def handle_upload(self, command_args):
        # Upload file implementation
        if len(command_args) < 2:
            self.request.sendall("Invalid upload command. Usage: upload <file_path>".encode())
            return

        file_path = command_args[1]
        if not os.path.isfile(file_path):
            self.request.sendall("File not found on the server".encode())
            return

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        self.request.sendall(f"upload {file_name} {file_size}".encode())

        current_dir = os.getcwd()
        abs_file_path = os.path.join(current_dir, file_name)

        with open(abs_file_path, "wb") as file:
            while True:
                data = self.request.recv(4096)
                if not data:
                    break
                file.write(data)

        print(f"File '{file_name}' uploaded successfully.")
        self.request.sendall("ACK".encode())  # Send acknowledgment to client
        self.request.recv(1024)
    def send_data(self, data):
        data_size = len(data)
        self.request.sendall(data_size.to_bytes(8, byteorder="big"))
        self.request.sendall(data)

    def handle_download(self, command_args):
        # Download file implementation
        if len(command_args) < 2:
            self.request.sendall("Invalid download command. Usage: download <file_path>".encode())
            return

        file_path = command_args[1]
        if not os.path.isfile(file_path):
            self.request.sendall("File not found on the server".encode())
            return

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Send the file data with the file size information in a single transmission
        with open(file_path, "rb") as file:
            file_data = file.read()

        data_to_send = f"download {file_name} {file_size}\n".encode() + file_data

        self.send_data(data_to_send)

        print(f"File '{file_name}' sent successfully.")


    def handle_help(self):
        # Help menu implementation
        help_msg = "\n".join([f"{cmd}: {description}" for cmd, description in COMMANDS.items()])
        self.request.sendall(help_msg.encode())

    def handle_shutdown(self):
        # Gracefully shut down the server
        print("Shutting down the server.")
        self.request.sendall("Server is shutting down.".encode())
        self.server.shutdown()

    def handle_end(self):
        # Close the server program entirely
        print("Closing the server program.")
        self.request.sendall("Server program is ending.".encode())
        self.server.shutdown()
        os.kill(os.getpid(), signal.SIGINT)

class MyTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, host, port):
        super().__init__((host, port), MyTCPHandler)
        self.host = host
        self.port = port

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
            self.server_close()

def get_local_ip():
    try:
        # Create a temporary socket to get the local IP address
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

if __name__ == "__main__":
    # Set the working directory to the location of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)

    HOST = get_local_ip()
    PORT = 65432

    server = MyTCPServer(HOST, PORT)
    server.start()
