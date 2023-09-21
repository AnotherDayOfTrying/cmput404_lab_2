import socket
from threading import Thread

class ProxyServer:
    """
    Proxy Server, performs the request received on behalf of the client
    
    client --> proxy --> server (1)
    client <-- proxy <-- server (2)
    """
    BYTES_TO_READ = 2**12 #4086
    def __init__(self, host, port) -> None:
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
    def start(self):
        """
        Starts Server (only able to handle a single request)
        """
        self.soc.bind((self.host, self.port))
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensure to allow address reuse as socket resources are not completely released when the socket is closed
        self.soc.listen()
        connection, address = self.soc.accept()
        self.handle_connection(connection, address)
        
    def start_threaded(self):
        """
        Starts Threaded Server (able to handle multiple requests from different clients)
        """
        self.soc.bind((self.host, self.port))
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.listen(2) # able to backlog 2 clients attempting to connect
        while True:
            connection, address = self.soc.accept()
            thread = Thread(target = self.handle_connection, args=[connection, address])
            thread.run()
    
    def send_request(self, host, port, request):
        """
        Send HTTP 1.1 request to a specified address (host, port)
        Args:
            host (string): host name (e.g. www.google.com)
            port (string): port number (e.g. 80)
            request (string): request to send to server

        Returns:
            string: response from server
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.send(request)
            client_socket.shutdown(socket.SHUT_WR)
            data = client_socket.recv(ProxyServer.BYTES_TO_READ)
            result = b"" + data
            while len(data) > 0:
                data = client_socket.recv(ProxyServer.BYTES_TO_READ)
                result += data
            return result
    
    def handle_connection(self, connection, address):
        """
        Handles a request made to the server. Echos back request to client.

        Args:
            connection (socket): Socket corresponding to the connected client
            address (_RetAddress): Address of the client
        """
        with connection:
            print(f"Connected by {address}")
            request = b""
            while True:
                data = connection.recv(ProxyServer.BYTES_TO_READ)
                if not data:
                    break
                print(data)
                request += data
            response = self.send_request("www.google.com", 80, request)
            connection.sendall(response)
        
    def __del__(self):
        self.soc.close() #send null byte to signify connection closed; ensure to close open socket when class is destroyed

HOST = "localhost" # 127.0.0.1
PORT = 8080

# Initialize Proxy Server
server = ProxyServer(HOST, PORT)

# Start Server
server.start() # Single Threaded
# server.start_threaded() # Multi-Threaded