import socket
from threading import Thread
from os import system

system("")
address = "localhost"
port = 10000
keywords = ["/dc","/roll","/flip","/me","/change","/learn","/help","/w"]

while True:
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    name = input("Enter username > ")
    if len(name.split()) != 1 :
        print("Name cannot contain spaces")
        continue
    name = name.strip()
    client_socket.connect((address,port))
    print("\nConnecting to server")
    client_socket.send(bytes(name,'utf-8'))
    response = client_socket.recv(256).decode()
    print("Server response: {}\n".format(response))
    
    if response == "Connection success":
        break
    else:
        client_socket.close()
print("Type \"/help\" for a list of commands")

def receive_message():
    while True:
        message = client_socket.recv(256).decode() 
        print(message)

t = Thread(target=receive_message)
t.daemon = True
t.start()

while True:
    data = input()
    print ("\033[A                             \033[A")
    args = data.split()
    if(args[0] in keywords):
        if args[0] == "/help":
            print("\n/roll  Generates a random number between 0-100")
            print("/flip    Flip a coin")
            print("/me      Perform an action in third person")
            print("/dc      Disconnect from the chatroom")
            print("/w       Send a private chat to other user")
            print("/change  Change user's current name")
            print("/learn   Get a random word and detail")
            print("/help    Show list of commands\n")


        if args[0] == "/me" and len(args) == 1:
            print("Invalid syntax for command /me")
            continue
        
        elif data == "/dc":
            client_socket.send(bytes(data,'utf-8'))
            break

        elif args[0] == "/dc" and len(args) > 1:
            print("Invalid syntax for command /dc")
            continue
        
        elif args[0] in ["/roll","/flip"] and len(args) > 1:
            print("Invalid syntax for command {}".format(args[0]))
            continue

        elif args[0] == "/learn" and len(args) > 1:
            print("Invalid syntax for command /learn")
            continue

        elif args[0] == "/w" and len(args) < 3:
            print("Invalid syntax for command {}".format(args[0]))
            continue

        elif args[0] == "/change" and (len(args) == 1 or len(args) > 2):
            print("Invalid syntax for command /change")
            continue
        
        if args[0] == "/change" and len(args) > 1  :
            args.pop(0)
            newname = "" 
            index = -1 
            for i in args:
                index += 1
                newname += i
                if index + 1 != len(args):
                    newname += " "
            name = newname
   
    else: 
        print('You('+name+'):'+data)

    client_socket.send(bytes(data,'utf-8'))
    