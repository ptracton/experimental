
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import AppConfig
import GUITools


class AppConfigGUI(QDialog):
    
    def __init__(self, parent = None):
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(AppConfigGUI, self).__init__(parent)
        print ("STARTING Config GUI")
        
        TopLayout = QVBoxLayout()
        self.XilinxPath = GUITools.PathOptionEditor(parent = self, name = "Xilinx Path")
        self.AlteraPath = GUITools.PathOptionEditor(parent = self, name = "Altera Path")

        ########################################################################
        #
        ########################################################################        
        PushButtonLayout = QHBoxLayout()
        self.OKButton = QPushButton("OK")
        self.CancelButton = QPushButton("Cancel")
        
        PushButtonLayout.addWidget(self.OKButton)
        PushButtonLayout.addWidget(self.CancelButton)

        QObject.connect(self.OKButton, SIGNAL("clicked()"), self.OKButtonClicked)
        QObject.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButtonClicked)

        TopLayout.addLayout(self.XilinxPath.GetLayout())
        TopLayout.addLayout(self.AlteraPath.GetLayout())
        TopLayout.addLayout(PushButtonLayout)
        
        self.setLayout(TopLayout)
        self.setWindowTitle("App Config Editor")
        
        return

    def OKButtonClicked(self):
        app = AppConfig.AppConfig()       
        app.AddSectionAndData("Xilinx", "Path", self.XilinxPath.LineEdit.text())
        app.AddSectionAndData("Altera", "Path", self.AlteraPath.LineEdit.text())
        app.AddSectionAndData("Projects", "Path", [])
        app.WriteFile()
        self.accept()
        return

    def CancelButtonClicked(self):
        self.reject()
        return
