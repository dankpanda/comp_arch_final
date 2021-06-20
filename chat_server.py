import socket
import threading
import random

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
        if msg.split()[0] == "/help":
            print(client_name + ": " + msg)

        elif msg == "/dc":
            current_clients.remove([client,client_name])
            print("-- {} has disconnected --".format(client_name))
            broadcast_all("-- {} has disconnected --".format(client_name))
            break

        elif msg == "/flip":
            result = random.choice(['HEADS','TAILS'])
            print("{} flipped \033[1m{}\033[0m".format(client_name,result))
            broadcast_all("{} flipped \033[1m{}\033[0m".format(client_name,result))

        elif msg == "/roll":
            result = random.randint(0,100)
            print("{} rolled \033[1m{}\033[0m".format(client_name,result))
            broadcast_all("{} rolled \033[1m{}\033[0m".format(client_name,result))
        
        elif msg.split()[0] == "/me":
            result = msg.split()
            result.pop(0)
            string = "* " + client_name + " "
            for i in result:
                string += i + " "
            string += "*"
            print("\033[3m {} \033[0m".format(string))
            broadcast_all("\033[3m {} \033[0m".format(string))

        else:
            message = client_name +': ' + msg
            print(message)
            broadcast(message,client)
    
def broadcast(message, sender): 
    for clients in current_clients: 
        if clients[0]!=sender:
            clients[0].send(bytes(message,'utf-8'))

def broadcast_all(message):
    for clients in current_clients:
        clients[0].send(bytes(message,'utf-8'))

while True:
    username_flag = False
    client, client_address = server_socket.accept()
    client_name = client.recv(256).decode()
    for i in current_clients:
        if i[1] == client_name:
            client.send(bytes('Username taken','utf-8'))
            username_flag = True
            break
    if username_flag == False:
        current_clients.append([client,client_name])
        threading._start_new_thread(new_thread,(client,client_address,client_name))
        client.send(bytes('Connection success','utf-8'))
    