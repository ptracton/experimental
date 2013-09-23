from PyQt4.QtCore import *
from PyQt4.QtGui import *

class OptionsBase(QWidget):
    """
    Base class for setting up a lot of GUI components
    """
    def __init__(self, parent = None, name = None):
        super(OptionsBase, self).__init__(parent)
        self.Layout = QHBoxLayout()
        self.Label = QLabel(name)
        self.Layout.addWidget(self.Label)
        return

    def GetLayout(self):
        return self.Layout    

class SimpleOptionEditor(OptionsBase):
    """
    """
    def __init__(self, parent = None, name = None):
        super(SimpleOptionEditor, self).__init__(parent, name = name)
        self.LineEdit = QLineEdit()
        self.Layout.addWidget(self.LineEdit)
        return

class PathOptionEditor(OptionsBase):
    """
    """
    def __init__(self, parent = None, name = None):
        super(PathOptionEditor, self).__init__(parent, name = name)

        self.LineEdit = QLineEdit()
        self.PathDialogButton = QPushButton("Path")

        self.Layout.addWidget(self.LineEdit)
        self.Layout.addWidget(self.PathDialogButton)
        QObject.connect(self.PathDialogButton, SIGNAL("clicked()"), self.ShowFileDialog)
        return

    def ShowFileDialog(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.LineEdit.setText(directory)

class FileOptionEditor(OptionsBase):
    """
    """
    def __init__(self, parent = None, name = None):
        super(FileOptionEditor, self).__init__(parent, name = name)

        self.LineEdit = QLineEdit()
        self.FileDialogButton = QPushButton("File")

        self.Layout.addWidget(self.LineEdit)
        self.Layout.addWidget(self.FileDialogButton)
        QObject.connect(self.FileDialogButton, SIGNAL("clicked()"), self.ShowFileDialog)
        return

    def ShowFileDialog(self):
        qfile = QFileDialog.getOpenFileName(self, 'Select or Create File', ".")
        self.LineEdit.setText(qfile)

class ListOptionEditor(OptionsBase):
    """
    """
    def __init__(self, parent = None, name = None):
        super(ListOptionEditor, self).__init__(parent, name)

        self.ComboBox = QComboBox()
        self.Layout.addWidget(self.ComboBox)

        return

class RadioButtonEditor(OptionsBase):
    """
    """
    def __init__(self, parent = None, name = None, count = 0, name_list = []):
        super(RadioButtonEditor, self).__init__(parent, name)

        self.GroupBox = QGroupBox(None)
        self.HBox = QHBoxLayout()

        for x in range(count):
            button = QRadioButton(name_list[x])
            button.setChecked(False)
            self.HBox.addWidget(button)
            del(button)

        self.GroupBox.setLayout(self.HBox)
        self.Layout.addWidget(self.GroupBox)
        return
