import socket
from threading import Thread

class Server:
    """
    Echo Server, sends back any bytes send to it (echos the request back to client)
    
    client --> server --> client (1)
    """
    BYTES_TO_READ = 2**12 #4086
    def __init__(self, host, port) -> None:
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # init server socket
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
        
    def handle_connection(self, connection, address):
        """
        Handles a request made to the server. Echos back request to client.

        Args:
            connection (socket): Socket corresponding to the connected client
            address (_RetAddress): Address of the client
        """
        with connection:
            print(f"Connected by {address}")
            while True:
                data = connection.recv(Server.BYTES_TO_READ)
                if not data: # recv will return None when client is finished send the HTTP request
                    break
                print(data)
                connection.sendall(data)
        
    def __del__(self):
        self.soc.close() # ensures to close open socket when class is destroyed

HOST = "localhost" # 127.0.0.1
PORT = 8080

# Initialize Echo Server
server = Server(HOST, PORT)

# Start Server
server.start() # Single Threaded
# server.start_threaded() # Multi Threaded