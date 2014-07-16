
from PyQt4.QtNetwork import *
import socket


__author__ = 'ptracton'

class IPAddress(QHostAddress):
    def __init__(self):
        super(IPAddress, self).__init__(None)
        self.__IPAddress = None


    def getAddress(self):
        return self.__IPAddress

    def findAddress(self):
        print (socket.gethostbyname(socket.gethostname()))
