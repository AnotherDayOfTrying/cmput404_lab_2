import socket

class ProxyClient:
    """
    Client to send requests to the PROXY SERVER
    """
    BYTES_TO_READ = 2**12 #4086
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
        self.soc.send(b"GET / HTTP/1.1\nHOST: www.google.com\n\n") # send HTTP 1.1 request
        self.soc.shutdown(socket.SHUT_WR) # note: sockets are duplex -> SHUT_WR means close write side
        result = self.soc.recv(ProxyClient.BYTES_TO_READ)
        while(len(result) > 0):
            print(result)
            result = self.soc.recv(ProxyClient.BYTES_TO_READ)
            
    def __del__(self):
        self.soc.close() #send null byte to signify connection closed
        
HOST = "localhost" # 127.0.0.1
PORT = 8080

# Initialize a Client
client = ProxyClient()

# Attempt to GET the specified address
client.get(HOST, PORT)

