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
    parser.add_argument("-s", help="auth file", type=str)
    parser.add_argument("-i", help="IP address", type=str)
    parser.add_argument("-n", help="new account balance", type=float)
    parser.add_argument("-d", help="deposit amount", type=float)
    parser.add_argument("-w", help="withdraw amount", type=float)
    parser.add_argument("-g", help="get account balance", action="store_true")
    parser.add_argument("-c", help="card number", type=str)

    args = parser.parse_args()

    # Create a client TCP socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    # TODO: replace the hardcoded IP and port with command line arguments
    //client_sock.connect(('127.0.0.1', 3000))
    client_sock.connect((args.s, args.p))

    # Send/receive some data
    # TODO: do something more interesting than send 'Hello world!'!
    # Note that Python's send and recv methods expect bytes! check out encode + decode methods
    if args.m:
        client_sock.sendall(args.m.encode())
    elif args.f:
        with open(args.f, 'rb') as f:
            client_sock.sendall(f.read())
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
