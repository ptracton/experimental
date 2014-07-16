
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import sys
import IPAddress
import Network_UI

class UI(QDialog, Network_UI.Ui_Dialog):
    def __init__(self, parent = None):
        super(UI, self).__init__(parent)
        self.setupUi(self)

        ##
        ## Get our hostname from the OS and update the label to display it
        ##
        hostInfo = QHostInfo()
        self.ipAddressLabel.setText(hostInfo.localHostName())
        self.localDomainLabel.setText(hostInfo.localDomainName())


        self.__IPAddress = IPAddress.IPAddress()
        self.__IPAddress.findAddress()


__author__ = 'ptracton'

app = QApplication(sys.argv)
form = UI()
form.show()
app.exec_()
