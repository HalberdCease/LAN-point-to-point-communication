import os,socket,sys,threading,time

port=int(sys.argv[1])
remote_user=sys.argv[2]

print("[start] 当前会话: 写字板")

wrbd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wrbd.connect(("127.0.0.1", port))

print("[connect] 会话已连接, 远程用户:",remote_user)

def main():
    while 1:
        str=input()
        wrbd.send(str.encode())
        os.system('cls')
        print("[start] 当前会话: 写字板")
        print("[connect] 会话已连接, 远程用户:",remote_user)

def chk_link():
    try:
        wrbd.recv(1024)
    except:
        os._exit(1)


t1=threading.Thread(target=main)
t2=threading.Thread(target=chk_link)
t1.start()
t2.start()