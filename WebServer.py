#coding: utf-8
import socket
import sys
import select
import re
import mimetypes
from pathlib import Path


if (len(sys.argv) != 2):
    print("Incorrect arguments")
    sys.exit

host = '127.0.0.1'
serverPort = int(sys.argv[1]) 
KEEP_ALIVE_TIMEOUT = 20
TIMEOUT = 20

print(f"Access via http://127.0.0.1:{serverPort}/ (CMD/CTRL + Click)")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, serverPort))
    s.listen()
    while True:
        conn, addr = s.accept()
        conn.settimeout(TIMEOUT)
        with conn:
            print(f"Connected by {addr}")
            alive = True
            while alive:
                try:
                    buffer = b""
                    while b"\r\n\r\n" not in buffer:
                        chunk = conn.recv(1024)
                        if not chunk:
                            break
                        buffer += chunk
                    data = buffer
                except socket.timeout:
                    print("Connection timed out - closing connection.")
                    break

                if not data:
                    print("Received empty packet - closing connection.")
                    break

                print(f"Received: {data[:20]}")
                if not re.match(b'GET .* HTTP/1.1', data):
                    print("Not a GET request.")
                    break
                file = re.findall(b'GET (.*) HTTP/1.1', data)[0][1:].decode()
                if file == '':
                    file = 'index.html'
                    content_type = 'text/html'
                if file == 'favicon.ico':
                    status = b"204 No Content"
                    content = b""
                    content_type = None
                if not Path(file).exists():
                    print(f"File {file} not found.")
                    status = b"404 Not Found"
                    content = b"Page Not Found!"
                    content_type = None
                else:
                    status = b"200 OK"
                    with open(file, 'rb') as f:
                        content = f.read()
                    content_type = mimetypes.guess_type(file)[0] or "application/octet-stream"

                header = b"HTTP/1.1 " + status + b"\r\n"
                header += b"Content-Length: " + str(len(content)).encode() + b"\r\n"
                if content_type:
                    header += b"Content-Type: " + content_type.encode() + b"\r\n"
                header += b"Connection: keep-alive\r\n"
                header += b"Keep-Alive: timout=" + str(KEEP_ALIVE_TIMEOUT).encode() + b"\r\n"
                header += b"\r\n"

                sentence = header + content
                conn.sendall(sentence)

                if re.search(b'Connection: close', data):
                    alive = False
                    print("Client requested connection close.")
