import socket
import time
import os
import signal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import queue
from PyQt5 import QtCore, QtGui, QtWidgets

class ClientManager():
        
    def __init__(self,host, port, messages):
        ipAddress = socket.gethostbyname(socket.gethostname())
        print('ipAddress: ',ipAddress)
        self.messages = messages
        self.host = host
        self.port = port

    def Working(self):
        self.ConnectToServer(self.host, self.port, self.messages)
        
    def ConnectToServer(self, host, port, messages):
        print('connect to server')
        socket_ = socket.socket()
        print('connect to: ',host)
        socket_.connect((host,port))
        message = bytes(messages, "utf-8") 
        try:
            for i in range(5):
                socket_.send(message)
                data = socket_.recv(1024)
                print("Server answer: ",data)
                time.sleep(1)
            socket_.close()       
        except:
            pass
def RunQThread(messages):
    host = '192.168.1.15'
    port = 8080
    for i in range(15):
        print(i)   
        messages = 'This is client: ' + str(i) 
        searchDataFromDataBase_thread = ClientManager(host, port, messages)
        searchDataFromDataBase_thread.Working()

    # searchDataFromDataBase_thread.setAutoDelete(True)
    # QThreadPool.globalInstance().start(searchDataFromDataBase_thread)
    
if __name__ == '__main__':
    host = '192.168.1.15'
    port = 8080
    # for i in range(5):
    #     print(i)
    messages = 'This is client: ' + str(0)
    RunQThread(messages)