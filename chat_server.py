import socket
import threading

address = "localhost"
port = 10000
current_clients = []

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((address,port))
server_socket.listen(5)
print('Server socket created successfully')

def new_thread(client, address, client_name):
    current_clients.append(client_name)
    print("-- {} joined the room --".format(client_name))
    while True:
        msg = client.recv(256).decode()
        if msg == "/dc":
            current_clients.remove(client_name)
            print("-- {} has disconnected --".format(client_name))
            break
        print(client_name + ": " + msg)

while True:
    client, client_address = server_socket.accept()
    client_name = client.recv(256).decode()
    if client_name in current_clients:
        client.send(bytes('Username taken','utf-8'))
    else:
        threading._start_new_thread(new_thread,(client,client_address,client_name))
        client.send(bytes('Connection success','utf-8'))
    