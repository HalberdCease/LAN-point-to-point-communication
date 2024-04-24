import socket
import psutil,os

username="Halberd_Cease"

if username.find('|')!=-1:
    print("[ERROR] 用户名不合法")
    exit()

def get_ip(name):
    return socket.gethostbyname(socket.gethostname())

def is_port_in_use(port):
    for proc in psutil.process_iter():
        for con in proc.connections():
            if con.status == 'LISTEN' and con.laddr.port == port:
                return True
    return False

ip=input("[input] 远程会话地址: ")

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((ip,11451))
except:
    print("[ERROR] 连接失败")
    client_socket.close()
    exit()

print("[connect] 正在和远程地址握手...")

cnt=21452
while is_port_in_use(cnt):
    cnt+=1
local_port=str(cnt)

print("[ok] 找到可用端口",local_port)

message_send=username+'|'+local_port

try:
    client_socket.send(message_send.encode())
except:
    print("[ERROR] 远端服务器意外结束 Socket 连接")
    client_socket.close()
    print("[close] 握手会话关闭")
    exit()
try:
    remote_message=client_socket.recv(1024).decode()
except:
    print("[ERROR] 远端服务器意外结束 Socket 连接")
    client_socket.close()
    print("[close] 握手会话关闭")
    exit()

remote_name=remote_message[0:remote_message.find('|')]

remote_port=remote_message[remote_message.find('|')+1:]

# print(ip,local_port,remote_port)

os.system("start cmd.exe /c python talk.py "+local_port+' '+remote_port+' '+ip+' '+remote_name)

print("[ok] 会话已建立")

client_socket.close()

print("[close] 握手会话关闭")