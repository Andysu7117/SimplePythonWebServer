#coding: utf-8
from socket import *
import sys

if (len(sys.argv) != 2):
    print("Incorrect arguments")
    sys.exit

serverPort = sys.argv[1] 

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

while 1:
    connectionSocket, addr = serverSocket.accept()

    sentence = connectionSocket.recv(1024)

    capitalizedSentence = sentence.upper()

    connectionSocket.send(capitalizedSentence)

    connectionSocket.close()
