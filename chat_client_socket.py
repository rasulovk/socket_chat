import time, socket, sys
import threading
 
socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 8181
 
# create a shared event to close all threading
# event = Event()

print('This is your IP address: ',ip)
# server_host = input('Enter friend\'s IP address:')
name = input('Enter Friend\'s name, name lenght could not be more than 6 character: ')

while True:
    if len(name) >=7:
        name = input('Enter Friend\'s name no more 6 character: ')
    elif len(name) ==0:
        name = input('Enter Friend\'s name no more 6 character and not empty: ')
    else:
        break

 
server_host = '127.0.0.1'
# name = 'samil'

socket_server.connect((server_host, sport))
 
socket_server.send(name.encode())
server_name = socket_server.recv(1024)
server_name = server_name.decode()
 
print(server_name,' has joined...')
# while True:
#     message = (socket_server.recv(1024)).decode()
#     print(server_name, ":", message)
#     message = input("Me : ")
#     socket_server.send(message.encode())

def recv_chat(socket_server,server_name):
    while True:
        message = (socket_server.recv(1024))
        if message:
            message = message.decode()
            print(server_name, ":", message)

def send_chat(socket_server):
    while True:
        message = input("Me : ")
        socket_server.send(message.encode())


client_handler_send = threading.Thread(target=send_chat, args=(socket_server,))
client_handler_recv = threading.Thread(target=recv_chat, args=(socket_server,server_name))
client_handler_send.start()
client_handler_recv.start()