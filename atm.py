#
# An ATM (client) in Python - CSCI 368
#
#

import sys
import argparse     # https://docs.python.org/3/library/argparse.html
import socket       # https://docs.python.org/3/library/socket.html
from os import _exit as quit

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="account name (required)")
    parser.add_argument("-p", help="port number", type=int)
    # TODO: add more arguments (check out the argparse docs)
    args = parser.parse_args()

    # Create a client TCP socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    # TODO: replace the hardcoded IP and port with command line arguments
    client_sock.connect(('127.0.0.1', 3000))


    # Send/receive some data
    # TODO: do something more interesting than send 'Hello world!'!
    # Note that Python's send and recv methods expect bytes! check out encode + decode methods
    client_sock.sendall(b'Hello world!')
    client_sock.shutdown(socket.SHUT_WR)

    chunks = []
    while True:
        data = client_sock.recv(2048)
        if not data:
            break
        chunks.append(data)
    print('Received', repr(b''.join(chunks)))

    # Disconnect from the server:
    client_sock.close()



if __name__ == "__main__":
    main()
