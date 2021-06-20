import socket
import threading

address = "localhost"
port = 10000
current_clients = []

print('Creating server socket')
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((address,port))
server_socket.listen(5)
print('Server socket created successfully')

def new_thread(client, address, client_name):
    print("-- {} joined the room --".format(client_name))
    broadcast_all("-- {} joined the room --".format(client_name))
    while True:
        msg = client.recv(256).decode()
        if msg == "/dc":
            current_clients.remove(client_name)
            print("-- {} has disconnected --".format(client_name))
            broadcast_all("-- {} has disconnected --".format(client_name))
            break
        message = client_name +': ' + msg
        print(message)
        broadcast(message,client)

def broadcast(message, sender): 
    for clients in current_clients: 
        if clients!=sender:
            clients.send(bytes(message,'utf-8'))

def broadcast_all(message):
    for clients in current_clients:
        clients.send(bytes(message,'utf-8'))

while True:
    client, client_address = server_socket.accept()
    client_name = client.recv(256).decode()
    if client_name in current_clients:
        client.send(bytes('Username taken','utf-8'))
    else:
        current_clients.append(client)
        threading._start_new_thread(new_thread,(client,client_address,client_name))
        client.send(bytes('Connection success','utf-8'))
    