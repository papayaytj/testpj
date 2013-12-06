#!/usr/bin/python

if __name__ == '__main__':
    import sys
    print sys.version
    import socket  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('10.61.3.213', 9099))  
    import time  
    time.sleep(1)  
    sock.send('1')  
    print sock.recv(1024)  
    sock.close()
