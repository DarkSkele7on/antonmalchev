import concurrent.futures
import urllib.request
import requests
from typing import List
import sys
import subprocess
import tempfile

class VPNClient:
    # Code for the VPNClient class goes here
    def __init__(self):
        # Fetch the list of VPN servers from the website
        response = requests.get('http://www.vpngate.net/api/iphone/')
        raw_data = response.text.replace('\r','')
        raw_servers = [line.split(',') for line in raw_data.split('\n')]

        # Extract the server labels and filter out any incomplete entries
        self.server_labels = raw_servers[1]
        self.server_labels[0] = self.server_labels[0][1:]
        self.servers = [srvrs for srvrs in raw_servers[2:] if len(srvrs) > 1]

    def connect_to_vpn(self, server: List[str]):
        # Extract the server IP address and port
        server_ip = server[1]
        server_port = server[2]

        # Generate the configuration file for the VPN server
        config_file = f"""
        remote {server_ip} {server_port}
        client
        dev tun
        proto udp
        """

        # Write the configuration file to a temporary file
        with tempfile.NamedTemporaryFile(mode="w+") as temp:
            temp.write(config_file)
            temp.seek(0)

            # Run the openvpn command with the configuration file, the --ca option, and the --cert and --key options
            subprocess.run(["openvpn", "--config", temp.name, "--ca", "<path-to-ca-file>", "--cert", "<path-to-client-certificate>", "--key", "<path-to-client-key>"])

    def filter_servers_by_country(self, country: str, j = 0) -> List[List[str]]:
        # Filter the list of servers by the given country
        return [server for server in self.servers if server[j] == country]
    def print_public_ip(self):
        response = requests.get("http://ipecho.net/plain")
        public_ip = response.text
        print(f"Public IP: {public_ip}")


class ThreadedPacketSender:
  def __init__(self, url, num_threads, num_packets):
    # Store the URL, number of threads, and number of packets
    self.url = url
    self.num_threads = num_threads
    self.num_packets = num_packets

  def send_packets(self, thread_id):
    # Loop through and send the specified number of packets
    for i in range(self.num_packets):
      # Send the packet to the URL using the urllib module
      urllib.request.urlopen(self.url)
      print("Thread {0}: Sent packet {1}".format(thread_id, i))

  def start(self):
    # Create a ThreadPoolExecutor with the specified number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
      # Start the threads in the pool
      for i in range(self.num_threads):
        executor.submit(self.send_packets, i)

    print("Finished sending packets")

# Use the VPNClient class to filter the list of servers by a given country
#if len(sys.argv) != 2:
#    print ('Enter one country at a time!')
#    exit(1)
#cntry = sys.argv[1]
#if len(cntry) > 2:
#    j = 5
#elif len(cntry) == 2:
#    j = 6
#else:
#    print ('Cannot identify the country. Name is too short.')
#    exit(1)

cntry = "Japan"
client = VPNClient()
country_servers = client.filter_servers_by_country(cntry)
client.connect_to_vpn(cntry)
client.print_public_ip()

threads = ThreadedPacketSender("google.com", 10, 10)
threads.start()