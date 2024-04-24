import os,threading,socket,sys,psutil,time

def get_ip(name):
    return socket.gethostbyname(socket.gethostname())

def is_port_in_use(port):
    for proc in psutil.process_iter():
        for con in proc.connections():
            if con.status == 'LISTEN' and con.laddr.port == port:
                return True
    return False

close=0

def start_write():
    port=19260
    while is_port_in_use(port):
        port+=1
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind(("127.0.0.1", port))
    host_socket.listen(1)
    os.system("start cmd.exe /c python writeboard.py "+str(port)+" "+remote_user)
    wbsc,address=host_socket.accept()
    host_socket.close()
    return wbsc

def remote():
    global close
    port=int(local_port)
    remote_ser=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ser.bind((get_ip(""),port))
    remote_ser.listen(1)
    remote_recv,address=remote_ser.accept()
    print("[connect] 远程会话已连接（读取）")
    while 1:
        try:
            data=remote_recv.recv(1024)
        except :
            print("[close] 远程会话关闭")
            os.system("start cmd.exe /c python err_close.py "+remote_user)
            os._exit(1)
        message=data.decode()
        print(remote_user+":",message)

def local():
    global close
    port=int(remote_port)
    ip=remote_ip

    wbsc=start_write()
    print("[connect] 本地写字板已连接")

    remote_send=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        remote_send.connect((ip,port))
    except:
        print("[ERROR] 远程会话连接失败（写入），重新连接[1/3]")
        try:
            remote_send.connect((ip,port))
        except:
            print("[ERROR] 远程会话连接失败（写入），重新连接[2/3]")
            try:
                remote_send.connect((ip,port))
            except:
                print("[ERROR] 远程会话连接失败（写入），重新连接[3/3]")
                try:
                    remote_send.connect((ip,port))
                except:
                    print("[ERROR] 远程会话连接失败（写入），终止连接")
                    os._exit(1)
    
    print("[connect] 远程会话已连接（写入）")

    while 1:
        try:
            data=wbsc.recv(1024)
        except :
            print("[ERROR] 写字板会话断开，重启写字板会话")
            wbsc=start_write()
            print("[connect] 本地写字板已连接")
            continue
        message=data.decode()
        print("You:",message)
        try:
            remote_send.send(data)
        except :
            print("[close] 远程会话关闭")
            close=1
            os.system("start cmd.exe /c python err_close.py "+remote_user)
            os._exit(1)

local_port=sys.argv[1]
remote_port=sys.argv[2]
remote_ip=sys.argv[3]
remote_user=sys.argv[4]
# print(local_port)
# print(remote_port)
# print(remote_ip)
print("[info] 远程用户:",remote_user)
t1=threading.Thread(target=remote)
t2=threading.Thread(target=local)
t1.start()
t2.start()
