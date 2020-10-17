import socket

HOST = '127.0.0.1'
PORT = 8000
clientMessage = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
while True:

    clientMessage = input("> ")
    

    client.sendall(clientMessage.encode('utf-8'))

client.close()
