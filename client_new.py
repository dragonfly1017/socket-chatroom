#!/usr/bin/env python3

import threading
import socket
import argparse
import os
import sys
import tkinter as tk


class Send(threading.Thread):
    """
    Sending thread listens for user input from the command line.

    Attributes:
        sock (socket.socket): The connected socket object.
        name (str): The username provided by the user.
    """
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        """
        Listens for user input from the command line only and sends it to the server.
        Typing 'QUIT' will close the connection and exit the application.
        """
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # Type 'QUIT' to leave the chatroom
            if message == '/quit':
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break
            
            # Send message to server for broadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))
        
        print('\nQuitting...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    """
    Receiving thread listens for incoming messages from the server.

    Attributes:
        sock (socket.socket): The connected socket object.
        name (str): The username provided by the user.
        messages (tk.Listbox): The tk.Listbox object containing all messages displayed on the GUI.
    """
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        """
        Receives data from the server and displays it in the GUI.
        Always listens for incoming data until either end has closed the socket.
        """
        while True:
            message = self.sock.recv(1024).decode('utf-8')

            if message:
                print('\r{}\n{}: '.format(message, self.name), end = '')
            
            else:
                # Server has closed the socket, exit the program
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:
    """
    Supports management of client-server connections and integration with the GUI.

    Attributes:
        host (str): The IP address of the server's listening socket.
        port (int): The port number of the server's listening socket.
        sock (socket.socket): The connected socket object.
        name (str): The username of the client.
        messages (tk.Listbox): The tk.Listbox object containing all messages displayed on the GUI.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None
    
    def start(self):
        """
        Establishes the client-server connection. Gathers user input for the username,
        creates and starts the Send and Receive threads, and notifies other connected clients.

        Returns:
            A Receive object representing the receiving thread.
        """
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))
        
        print()
        self.name = input('Your name: ')

        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        # Start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. Say hi!'.format(self.name).encode('ascii'))
        print("\rAll set! Leave the chatroom anytime by typing '/quit'\n")
        print('{}: '.format(self.name), end = '')

        return receive


def main(host, port):
    """
    Initializes and runs the GUI application.

    Args:
        host (str): The IP address of the server's listening socket.
        port (int): The port number of the server's listening socket.
    """
    client = Client(host, port)
    client.start()


main('127.0.0.1', 8000)