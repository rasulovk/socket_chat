# Requirments external library - redisdb
# pip install redis or pip3 install redis
#Imports the necessary libraries (redis, time, socket, threading, sys).
import time, socket
import redis
import threading
import sys

#Defines the server's IP address and port number for communication.
host_ip = '127.0.0.1'
#Create socket object
new_socket = socket.socket()
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)


#Initializes a Redis database instance to store client information.
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


# name = input('Enter name: ')
#Name of the Server which will be show in chat
name = 'ChatROOM_SRV'


#Defines a function to receive chat messages from clients and broadcasts them to all other clients.
def recv_chat(chat,client_name,src_port):
    while True:
        message = chat.recv(1024)
        if message:
            message = message.decode()
            print(client_name, ':', message)
            #Get hash from hset : structure of hset hset('hash','key','value')
            #hash contain uniqiue source port of each connected client
            for k in r.keys():
                # print(f"Source port is: {k}")
                # print(f"Current port passed to function is {src_port}")
                #Do not return message back to sender. Unique client source port added to this function in thread.
                if src_port != int(k):
                    #Get key value by the loop hash value of hset
                    for i in r.hkeys(k):
                        stored_chat_id = int(r.hget(k,i))
                        modified_message = f"From {r.hkeys(k)} : {message}" 
                        # print(f'Compared value is {src_port}  ---   {int(k)}')
                        client_socket = socket.fromfd(stored_chat_id, socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.send(modified_message.encode())


#Defines a function to send chat messages to the server and broadcasts them to all other clients
def send_chat(chat):
    while True:
        message = input('Me : ')
        chat.send(message.encode())
        try:
            #Get hash from hset : structure of hset hset('hash','key','value')
            #hash contain uniqiue source port of each connected client
            for k in r.keys():
                # print(f"Source port is: {k}")
                # print(f"Current port passed to function is {src_port}")
                #Get key value by the loop hash value of hset
                for i in r.hkeys(k):
                    # get socket object by r.hget(k,i) : where is 'k' is client source port, 'i' is client name
                    stored_chat_id = int(r.hget(k,i))
                    #Before forward to other user add recepient name to message
                    modified_message = f"From ChatROOM_SRV To {r.hkeys(k)} : {message}" 
                    client_socket = socket.fromfd(stored_chat_id, socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.send(modified_message.encode())
        except:
            pass


#Defines a function to handle new client connections, store client information in Redis, and create threads for sending and receiving messages.
def handle_client(client_con, src_port):
    client = (client_con.recv(1024)).decode()
    print(client + ' has connected.')
    client_con.send(name.encode())
    # store_in_redis(src_port,client_con,client)
    # r.set(src_port,client_con.fileno())
    r.hset(src_port, client, client_con.fileno())
    #Handles new client connections by creating a new thread to handle each client and passing the client's information to Redis.
    client_handler_send = threading.Thread(target=send_chat, args=(client_con,))
    client_handler_recv = threading.Thread(target=recv_chat, args=(client_con,client,src_port))
    client_handler_send.start()
    client_handler_recv.start()

#Binds the socket to the server's IP address and port number and listens for new connections.
port = 8181
new_socket.bind((host_ip, port))
new_socket.listen(3)
print(f"Binding successful on port {port}!")
print("This is your IP: ", s_ip)
 
#Main loop
while True:
    try:
        #Wait for new coonection in while loop
        client_con, add = new_socket.accept()
        for i in range(len(add)):
            print(f"New connection by index {i} : {add[i]}")
        handle_client(client_con,add[i])
    #Dec
    except KeyboardInterrupt:
        #Cleans up Redis database on server shutdown.
        for i in r.keys():
            r.delete(i)
        print('interrupted!')
        sys.exit(0)