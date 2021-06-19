import socket
import threading

address = "localhost"
port = 10000

while True:
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    name = input("Enter username > ")
    client_socket.connect((address,port))
    print("Connecting to server")
    client_socket.send(bytes(name,'utf-8'))
    response = client_socket.recv(256).decode()
    print("Server response: {}".format(response))
    
    if response == "Connection success":
        break
    else:
        client_socket.close()
print("Type \"/dc\" to disconnect")

while True:
    data = input('> ')
    client_socket.send(bytes(data,'utf-8'))
    if(data == "/dc"):
        break
    data_response = client_socket.recv(256).decode()
    print('chatbot: '+ data_response)