import socket

def scan_ports(ip, port_range):
  for port in range(port_range[0], port_range[1]):
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(0.5)
      result = sock.connect_ex((ip, port))
      if result == 0:
        print("Port {} is open".format(port))
      sock.close()
    except:
      pass

ip = input("Enter target ip: ")
port_range = (1, 65535) # enter the range of ports you want to scan
scan_ports(ip, port_range)