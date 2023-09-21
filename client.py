import socket

class Client:
    """
    Client to connect to ECHO SERVER
    """
    BYTES_TO_READ = 2**12 # 4086
    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4; SOCK_STREAM = TCP
        
    def get(self, host, port):
        """
        Send HTTP 1.1 request to a specified address (host, port)
        Args:
            host (string): host name (e.g. www.google.com)
            port (string): port number (e.g. 80)
        """
        self.soc.connect((host, port))
        self.soc.send(b"GET / HTTP/1.1\nHOST: " + host.encode("utf-8") + b"\n\n") # send HTTP 1.1 request
        self.soc.shutdown(socket.SHUT_WR) # sockets are duplex -> SHUT_WR means close write side
        result = self.soc.recv(Client.BYTES_TO_READ)
        while(len(result) > 0):
            print(result)
            result = self.soc.recv(Client.BYTES_TO_READ)
            
    def __del__(self):
        self.soc.close() #send null byte to signify connection closed; ensure to close open socket when class is destroyed

# LOCALHOST TESTING
HOST = "localhost" # alias for 127.0.0.1
PORT = 8080

# TESTING GOOGLE.COM
# HOST = "www.google.com"
# PORT = 80

# Initialize a Client
client = Client()

# Attempt to GET the specified address
client.get(HOST, PORT)

