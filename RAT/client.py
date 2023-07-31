import socket
import time
import zlib
import os

EXIT_COMMAND = "exit"

class MyTCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.command_history = []

    def connect(self):
        MAX_RETRIES = 5
        retry_count = 0

        while retry_count < MAX_RETRIES:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.server_ip, self.server_port))
                print("Connected to the server. Type 'exit' to close the connection.")
                return True

            except ConnectionRefusedError:
                print(f"Connection refused. Retrying ({retry_count + 1}/{MAX_RETRIES})...")
                retry_count += 1
                time.sleep(2)

            except socket.error as e:
                print(f"Socket error: {e}")
                return False

            except Exception as e:
                print(f"Error: {e}")
                return False

        print("Failed to connect to the server. Maximum retries reached.")
        return False

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")
        else:
            print("Not connected to any server.")

    def send_command(self, command):
        try:
            self.client_socket.sendall(command.encode())
            self.client_socket.settimeout(5)  # Set a timeout of 5 seconds for recv()
            response = self.client_socket.recv(4096)
            self.client_socket.settimeout(None)  # Reset the timeout after receiving
            if response.startswith(b"Error"):
                print(response.decode())
                return None
            return response
        except socket.timeout:
            print("Server response timeout.")
            return None
        except socket.error as e:
            print(f"Socket error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def recv_data(self, size):
        data = b""
        while size > 0:
            packet = self.client_socket.recv(min(size, 4096))
            if not packet:
                return None
            data += packet
            size -= len(packet)
        return data

    def execute(self):
        try:
            while True:
                command = input("Enter the command to execute on the server: ")

                if not command.strip():
                    continue  # Skip empty commands

                if command.strip().lower() == EXIT_COMMAND:
                    self.send_command(command)
                    break
                else:
                    self.command_history.append(command.strip())
                    response = self.send_command(command)

                    if response:
                        if command.startswith("download"):
                            try:
                                # Extract the file name and size from the response
                                file_info = response.decode().split()
                                file_name = file_info[1]
                                file_size = int(file_info[2])

                                # Receive the file data from the server
                                file_data = self.recv_data(file_size)

                                # Get the current working directory
                                current_dir = os.getcwd()
                                # Construct the full download path
                                download_location = os.path.join(current_dir, file_name)

                                # Save the received file data to the download location in binary mode
                                with open(download_location, "wb") as file:
                                    file.write(file_data)

                                print(f"File '{file_name}' downloaded successfully to: {download_location}")
                            except Exception as e:
                                print(f"Error during file download: {e}")
                        else:
                            print("Server response:", response.decode())

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.disconnect()


if __name__ == "__main__":
    # Set the working directory to the location of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)

    SERVER_IP = "172.20.10.4"
    SERVER_PORT = 65432

    client = MyTCPClient(SERVER_IP, SERVER_PORT)
    if client.connect():
        client.execute()
