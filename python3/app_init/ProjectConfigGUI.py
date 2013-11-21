#! /usr/bin/env python3

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import AppConfig
import GUITools
import ProjectConfig

class ProjectConfigGUI(QDialog):
    
    def __init__(self, parent = None):
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(ProjectConfigGUI, self).__init__(parent)
        print ("STARTING Project Config GUI")
        
        TopLayout = QVBoxLayout()

        ########################################################################
        #
        # Top Level Options
        #
        ######################################################################## 
        self.ProjectNameLayout = GUITools.SimpleOptionEditor(name = "Project Name")
        self.TestBenchNameLayout = GUITools.SimpleOptionEditor(name = "Test Bench Name")
        self.TestBenchInstanceNameLayout = GUITools.SimpleOptionEditor(name = "Test Bench Instance Name")
        self.TopLevelModuleLayout = GUITools.SimpleOptionEditor(name = "Top Level Module")
        self.CPULayout = GUITools.ListOptionEditor(name = "CPU Selection")
        
        ## TEMP HACK UNTIL WE BRING IN REAL INFO FROM ELSEWHERE!        
        self.CPULayout.ComboBox.insertItems(3, ["Picoblaze", "OpenMSP430", "OR1200"])        
        self.TechnologyLayout = GUITools.RadioButtonEditor(name = "Technology Selection", count =3, name_list=["Xilinx", "Altera", "ASIC"])
        ## END TEMP HACK

        ########################################################################
        #
        # OK/Cancel Buttons
        #
        ########################################################################        
        self.ProjectFileLayout = GUITools.FileOptionEditor(name = "Project Config File")

        PushButtonLayout = QHBoxLayout()
        self.OKButton = QPushButton("OK")
        self.CancelButton = QPushButton("Cancel")
        
        PushButtonLayout.addWidget(self.OKButton)
        PushButtonLayout.addWidget(self.CancelButton)

        QObject.connect(self.OKButton, SIGNAL("clicked()"), self.OKButtonClicked)
        QObject.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButtonClicked)

        ########################################################################
        #
        # Put all the parts together
        #
        ######################################################################## 
        TopLayout.addLayout(self.ProjectNameLayout.GetLayout())
        TopLayout.addLayout(self.TestBenchNameLayout.GetLayout())
        TopLayout.addLayout(self.TestBenchInstanceNameLayout.GetLayout())
        TopLayout.addLayout(self.TopLevelModuleLayout.GetLayout())
        TopLayout.addLayout(self.CPULayout.GetLayout())
        TopLayout.addLayout(self.ProjectFileLayout.GetLayout())
        TopLayout.addLayout(self.TechnologyLayout.GetLayout())

        TopLayout.addLayout(PushButtonLayout)
        
        self.setLayout(TopLayout)
        self.setWindowTitle("Project Config Editor")
        
        return

    def OKButtonClicked(self):

        ConfigFile = self.ProjectFileLayout.LineEdit.text()

        Config = ProjectConfig.ProjectConfig()
        
        if (Config.ConfigExists(ConfigFile)):
            print ("Already exists, read, mod, write !")
        else:
            Config.AddSectionAndData("General Project", 
                                     "Project Name", 
                                     self.ProjectNameLayout.LineEdit.text())

            Config.AddSectionAndData("General Project", 
                                     "Test Bench Name", 
                                     self.TestBenchNameLayout.LineEdit.text())

            Config.WriteFile()

        self.accept()
        return

    def CancelButtonClicked(self):
        self.reject()
        return


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = ProjectConfigGUI()
    gui.show()
    app.exec_()    
    
    pass
