import socket
import threading
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

print('Setting up the chatbot')
chatbot=ChatBot('chat bot')  
trainer_chatbot = ChatterBotCorpusTrainer(chatbot)

print('Training the chatbot')
trainer_chatbot.train("chatterbot.corpus.english")
trainer_chatbot.train("chatterbot.corpus.english.greetings")
trainer_chatbot.train("chatterbot.corpus.english.conversations")

address = "localhost"
port = 10000
current_clients = []

print('Creating server socket')
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
        if msg.startswith("/bot "):
            msg_response = str(chatbot.get_response(msg.split('/bot')[1]))
            client.send(bytes(msg_response,'utf-8'))
            print('chatbot to '+ client_name +': ' + msg_response)

while True:
    client, client_address = server_socket.accept()
    client_name = client.recv(256).decode()
    if client_name in current_clients:
        client.send(bytes('Username taken','utf-8'))
    else:
        threading._start_new_thread(new_thread,(client,client_address,client_name))
        client.send(bytes('Connection success','utf-8'))
    