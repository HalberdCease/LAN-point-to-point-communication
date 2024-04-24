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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((get_ip('ens36'), 11451))

print("[start] 服务器开始监听...")
print("[info] ip:",get_ip('ens36'))

while(1):
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    ip,port=client_address

    print("[connect] 连接申请，来自",ip)

    remote_message=client_socket.recv(1024).decode()

    remote_name=remote_message[0:remote_message.find('|')]

    remote_port=remote_message[remote_message.find('|')+1:]

    cnt=11452
    while is_port_in_use(cnt):
        cnt+=1
    local_port=str(cnt)
    print("[ok] 找到可用端口",cnt)

    message_send=username+'|'+local_port

    try:
        client_socket.send(message_send.encode())
    except:
        print("[ERROR] 远端客户端意外结束 Socket 连接")
        client_socket.close()
        print("[close] 握手会话关闭")
        continue

    os.system("start cmd.exe /c python talk.py "+local_port+' '+remote_port+' '+ip+' '+remote_name)
    print("[ok] 会话已建立")
    client_socket.close()
    print("[close] 握手会话关闭")
    
server_socket.close()
