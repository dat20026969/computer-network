# DO AN SOCKET MON MANG MAY TINH:
# LE DUC DAT 20127674
# VO MINH ANH 20127441

import socket
import threading #da luong
import requests
from requests.structures import CaseInsensitiveDict
import json

TEAMDATANH_HOSTNAME="WEWINASONE-PC"
HOST = '127.0.0.1' 
HEADER = 64
PORT = 60000
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def recvList(conn):
    list = []
    item = conn.recv(9999999).decode(FORMAT)
    while (item != "end"):

        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(9999999).decode(FORMAT)

    return list

def handleClient(conn: socket, addr):
    print("Duoc ket noi boi: ", conn.getsockname())
    bank = None
    while (bank != "x"):
        bank = conn.recv(9999999).decode(FORMAT)
        print("client ", addr, "says", bank)
        if (bank == "VCB"):
            conn.sendall(bank.encode(FORMAT))
            list = recvList(conn)
            print("received: ")
            print(list)
            print("VNBankName: ", bank)
            url = "https://vapi.vnappmob.com/api/v2/exchange_rate/vcb"
            headers = CaseInsensitiveDict()
            headers["Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzAxNDgzMDgsImlhdCI6MTYyODg1MjMwOCwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.bQxV1_UnpTlS7qqRMPFgNti3Qlhotq0rmZdhv34pDdU"
            resp = requests.get(url, headers=headers)
            x = resp.json()["results"]
            data=resp.json()
            conn.sendall(bytes(str(data), encoding="utf-8"))
            for i in range(0, len(x)):
                print("Tien te: ",               x[i]['currency'])
                print("Mua vao: ",               x[i]['buy_cash'])
                print("Chuyen doi: ",            x[i]['buy_transfer'])
                print("Ban ra: ",                x[i]['sell'])
                print("*************************")
                # conn.sendall(data.decode(FORMAT))
                

    print("client", addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()
#---------------------------------------------------#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))  # Đăng ký tên cho socket, ràng buộc địa chỉ vào socket, để host server trên địa chỉ mà mình khai báo.
# Chức năng chỉ mở lên và đợi connection.
s.listen(5)  # Cho socket đang lắng nghe tới tối đa 5 kết nối, đợi
print("Server listening on port", PORT)
print("***SERVER***")
print("Server: ", HOST, PORT)
print("Waiting for the client to connect .-.-.-.-.")

nClient=0
while(nClient<3):
    try:
        conn, addr = s.accept()
        # Khi một client gõ cửa, server chấp nhận kết nối và 1 socket mới được tạo ra. Client và server bây giờ đã có thể truyền và nhận dữ liệu với nhau, lập tức trả về 2 biến là address và connection.
        # conn: Trao đổi thông tin, gửi/nhận thông tin, gửi dữ liệu thật sự trên đường truyền.
        thre = threading.Thread(target=handleClient, args=(conn, addr))
        thre.daemon = False
        thre.start()
        
    except Exception as e:
        print(e)
    nClient += 1
print("End")
s.close()

