#coding: utf-8
from socket import *
import sys

if (len(sys.argv) != 2):
    print("Incorrect arguments")
    sys.exit

serverPort = int(sys.argv[1]) 

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

while 1:
    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(1024).decode()

    print("Request: \n", request)

    response_body = "Hello from the server"
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{response_body}"
    )

    connectionSocket.sendall(response.encode())
    connectionSocket.close()
