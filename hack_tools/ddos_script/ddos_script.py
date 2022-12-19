import concurrent.futures
import urllib.request
from typing import List
import socket

class ThreadedPacketSender:
  def __init__(self, url: str, num_threads: int, num_packets: int):
    # Store the URL, number of threads, and number of packets
    self.url = url
    self.num_threads = num_threads
    self.num_packets = num_packets

  def send_packets(self, thread_id: int):
    # Loop through and send the specified number of packets
    for i in range(self.num_packets):
      # Send the packet to the URL using the urllib module
      urllib.request.urlopen(self.url)
      print("Thread {0}: Sent packet {1}".format(thread_id, i))

  def start(self):
    # Get the IP address of the target website
    target_ip = socket.gethostbyname(self.url)
    print("Target IP: {0}".format(target_ip))

    # Create a ThreadPoolExecutor with the specified number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
      # Start the threads in the pool
      for i in range(self.num_threads):
        executor.submit(self.send_packets, i)

    print("Finished sending packets")
ip = input("Enter target addres: ")
threads = ThreadedPacketSender(ip, 10, 10)
threads.start()