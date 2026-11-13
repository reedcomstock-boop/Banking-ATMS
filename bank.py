#
# A bank (server) in Python - CSCI 368
# Adapted from Ivan Velichko's TCP Sockets Tutorial
# Any/all of this code can be 

import sys
import socket
from os import _exit as quit

def main():
    # TODO: parse arguments (see example in atm.py)

    # Set up socket
    serv_sock = socket.socket(
        socket.AF_INET,      # IPv4 Internet socket
        socket.SOCK_STREAM,  # stream-oriented socket
        proto=0              # choose the default protocol: TCP for AF_INET + SOCK_STREAM
    )

    # Bind to socket and start listening
    # TODO: replace the hardcoded port with command line arguments
    serv_sock.bind(('127.0.0.1', 3000))
    serv_sock.listen(10) # argument determines max number of queued connections

    # Main loop: accept a connection, receive, send
    while True:
        # accept a new connection from the backlog queue
        client_sock, client_addr = serv_sock.accept()
        print(f"client address: {client_addr}")

        # message loop
        # TODO: do something more interesting than echo data back!

        chunks = []
        while(True):
            #Note: Python's send and recv methods expect bytes! check out encode + decode methods
            data = client_sock.recv(2048)
            if not data:
                break
            chunks.append(data)

        client_sock.sendall(b''.join(chunks))
        client_sock.close()


if __name__ == "__main__":
    main()
