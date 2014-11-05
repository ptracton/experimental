
from PyQt4.QtNetwork import *
import subprocess
import platform
import re
import socket

__author__ = 'ptracton'


class IPAddress(QHostAddress):

    def __init__(self):
        super(IPAddress, self).__init__(None)
        self.__IPAddress = None
        self.__system = platform.system()
        self.findAddress()

    def getAddress(self):
        return self.__IPAddress

    def findAddress(self):
        if (self.__system == "Windows"):
            self.__IPAddress = socket.gethostbyname(socket.getfqdn())

        if (self.__system == "Linux"):
            (dist, version, name) = platform.linux_distribution()
            print (dist)
            if (dist == "LinuxMint"):
                self.__IPAddress = subprocess.check_output(["hostname",
                                                            "-I"]).decode("utf-8")
            if (dist == "RedHat"):
                self.__IPAddress = subprocess.check_output(["hostname",
                                                            "-i"]).decode("utf-8")

        print ("IP ADDR:  %s" % self.__IPAddress)
        f = QNetworkInterface()
        print ("FOO: " + f.hardwareAddress())
