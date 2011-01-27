import socket,time

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.110.8',8782))
    sock.send('111')
    r = sock.recv(2048)
    print r
    time.sleep(100)