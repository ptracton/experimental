#! /usr/bin/env python3

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import AppConfig
import GUITools
import ProjectConfig
import VerilogParse

class IPConfigGUI(QDialog):
    
    def __init__(self, parent = None):
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(IPConfigGUI, self).__init__(parent)
        print ("STARTING IP Config GUI")
        
        TopLayout = QVBoxLayout()

        ########################################################################
        #
        # File Dialog and OK/Cancel
        #
        ########################################################################        
        self.ProjectFileLayout = GUITools.FileOptionEditor(name = "Verilog File")

        PushButtonLayout = QHBoxLayout()
        self.OKButton = QPushButton("OK")
        self.CancelButton = QPushButton("Cancel")
        
        PushButtonLayout.addWidget(self.OKButton)
        PushButtonLayout.addWidget(self.CancelButton)

        QObject.connect(self.OKButton, SIGNAL("clicked()"), self.OKButtonClicked)
        QObject.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButtonClicked)

        TopLayout.addLayout(self.ProjectFileLayout.GetLayout())

        TopLayout.addLayout(PushButtonLayout)
        
        self.setLayout(TopLayout)
        self.setWindowTitle("IP Config Editor")
        
        return
    def OKButtonClicked(self):

        ConfigFile = self.ProjectFileLayout.LineEdit.text()

        print(ConfigFile)
        parser = VerilogParse.VerilogParse(FileName = ConfigFile)
        parser.GetPorts()
        self.accept()
        return

    def CancelButtonClicked(self):
        self.reject()
        return


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = IPConfigGUI()
    gui.show()
    app.exec_()    
    
    pass
