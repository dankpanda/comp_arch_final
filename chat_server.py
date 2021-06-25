import socket
import threading
import random
import os
from PyDictionary import PyDictionary

os.system("")
address = "localhost"
port = 10000
current_clients = []


dictionary = PyDictionary()
#get random word

#get definition of word

file = open("words.txt", "r", encoding='utf-8')
words = file.read().split("\n")


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

        elif msg.split()[0] == "/w":
            receiver = msg.split()[1]
            whisper_msg = msg.split()
            for i in range(2):
                whisper_msg.pop(0)
            whisper_msg = " ".join(whisper_msg)
            client_msg = "You whisper to "+ receiver +": "+whisper_msg
            message = client_name + " whisper to You: " + whisper_msg
            print(client_name + " whisper to " + receiver + ": " + whisper_msg)
            client.send(bytes(client_msg,'utf-8'))
            whisper(message,receiver,client)

        elif msg.split()[0] == "/change":
            result = msg.split()
            result.pop(0)
            newname = "" 
            index = -1 
            for i in result:
                index += 1
                newname += i
                if index + 1 != len(result):
                    newname += " "

            print("-- {} Updated from {} --".format(newname, client_name))
            broadcast_all("-- {} Updated from {}--".format(newname, client_name))
            
            current_clients.remove([client,client_name])
            current_clients.append([client,newname])
            client_name = newname

        elif msg == "/learn":
            print(define_word())
            broadcast_all(define_word())
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
        

def whisper(message, receiver, sender):
    valid_name = False
    for clients in current_clients:
        if clients[1]==receiver:
            valid_name = True
            clients[0].send(bytes(message,'utf-8'))
            break
    if valid_name == False:
        for clients in current_clients:
            if clients[0]==sender:
                clients[0].send(bytes('\033[A                             \033[A\nUsername is not found in the chatroom','utf-8'))

def get_word():
    valid_word =False
    while(not valid_word):
        index = random.randint(0,466551)
        word = words[index]

        if(word[0].islower() and len(word)>2): 
            valid_word = True
            return word

def define_word():
    valid_word = False
    while(not valid_word):
        word = get_word()
        if(dictionary.meaning(word, disable_errors = True)):
            print(str(word.upper() + "\n"))
            defs = dictionary.meaning(word)

            for key, value in defs.items():
                d = (str(str(key)+": "+str(value).strip("[]\'\"").replace("\'","")))

            syns = dictionary.synonym(word)
            if syns:
                s = ""
                for syn in syns:
                    s+= syn+", "
                b = (str("\n" + "Synonyms: "+s[:-2]+"\n"))

            ants = dictionary.antonym(word)
            if ants:
                a = ""
                for ant in ants:
                    s+= ant+", "
                c = (str("Antonyms: " +a[:-2]))

            print(broadcast_all(str(d)))     
            print(broadcast_all(str(b)))   
            print(broadcast_all(str(c)))  
            valid_word = True
    

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
    