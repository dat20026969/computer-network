import socket
import threading
import requests
from requests.structures import CaseInsensitiveDict
import json

HOST = '127.0.0.1'  # loopback: de tro ve dia chi may minh`.
HEADER = 64
PORT = 60000 #Muon server minh` mo tren cai port tren cai may minh` > 50000
FORMAT = 'utf8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def sendList(client, list):

    for item in list:
        client.sendall(item.encode(FORMAT))
        #wait response
        client.recv(1024)

    msg = "end"
    client.send(msg.encode(FORMAT))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Khai bao Socket, trong do:
# SOCK_STREAM: Giao thuc TCP
# AF_INET: IPv4 
server_address = (HOST, PORT)
print("***CLIENT***")
try:
    client.connect(server_address)
    print("Ket noi thanh cong!")
    print("Dia chi client: ", client.getsockname())
    list=["VCB"]
    bank=None
    while (bank!="x"):
        bank = input("Ten ngan hang: ")
        client.sendall(bank.encode(FORMAT)) #encode: gui 1 tin nhan tren Socket
        if(bank=="VCB"):
            client.recv(99999)
            sendList(client, list)

except:
    print("Error")

client.send(DISCONNECT_MESSAGE)

client.close()
