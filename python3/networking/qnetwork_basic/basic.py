#! /usr/bin/env python3

import socket
from PyQt4 import QtNetwork

if __name__ == "__main__":
    hostInfo = QtNetwork.QHostInfo()
    hostAddress = QtNetwork.QHostAddress()
    hostAddress.setAddress(socket.gethostbyname(socket.gethostname()))
    print(socket.gethostbyname(socket.gethostname()))
    print(hostAddress.toString())
