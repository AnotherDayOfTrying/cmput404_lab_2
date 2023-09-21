# CMPUT 404 LAB 2

Assuming the use of python 3.11+ sockets will be builtin. Thusly, no requirements.txt is provided.

## Question 1: How do you specify a TCP socket in Python?

You can create a TCP socket by setting the socket type to `SOCKET.SOCK_STREAM`.

## Question 2: What is the difference between a client socket and a server socket in Python?

The client socket will send requests and read the response. A server socket will listen for incoming requests to connect and handle those incoming requests. The server socket is required to bind to a port number to list to incoming client requests.

## Question 3: How do we instruct the OS to let us reuse the same bind port?

We use the following snippet:
`soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`

We need to allow reuse of the same bind port because the socket resources are not completely released when the socket is closed. This means when we want to re-run or restart the server, we have to wait until these resources are properly released. We can re-use the same port number to prevent this from happening.

## Question 4: What information do we get about incoming connections?

We get the `IP` and the `PORT` of any incoming connections.

## Question 5: What is returned by recv() from the server after it is done sending the HTTP request?

After an HTTP request is finished sending, the sender will send a NULL byte to signify the end of the request. The recv() function on the other end, at the receiver, will return None. We can use this to know when the request is completely sent.

## Question 6: Provide a link to your code on GitHub.

https://github.com/AnotherDayOfTrying/cmput404_lab_2