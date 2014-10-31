'''
Created on Apr 8, 2013

@author: tractp1
'''

import random
from PyQt4 import QtGui
from PyQt4 import QtCore
import QtMpl


class UI(QtGui.QMainWindow):

    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #
        # initialization of Qt MainWindow widget
        #
        QtGui.QMainWindow.__init__(self)

        #
        # set window title
        #
        self.setWindowTitle("Matplotlib and QT4")

        #
        # instantiate a widget, it will be the main one
        #
        self.main_widget = QtGui.QWidget(self)

        #
        # Connect out top level layout to the main_widget
        #
        top_layout = QtGui.QVBoxLayout(self.main_widget)

        #######################################################################
        #
        # Matplotlib object
        #
        #######################################################################
        self.mpl = QtMpl.QtMpl(self.main_widget)
        top_layout.addWidget(self.mpl)
        self.line_count = 0

        #######################################################################
        #
        # Add in 2 buttons.  Add a line and remove a line which do just this
        # to the matplotlib graph
        #
        #######################################################################
        self.add_button = QtGui.QPushButton("Add a line")
        self.remove_button = QtGui.QPushButton("Remove a line")
        top_layout.addWidget(self.add_button)
        top_layout.addWidget(self.remove_button)

        # Connect signals to make things happen
        self.connect(self.add_button, QtCore.SIGNAL("clicked()"), self.updateAddButton)
        self.connect(self.remove_button, QtCore.SIGNAL("clicked()"), self.updateRemoveButton)

        #
        # set the focus on the main widget
        #
        self.main_widget.setFocus()

        #
        # set the central widget of MainWindow to main_widget
        #
        self.setCentralWidget(self.main_widget)

        return

    def updateAddButton(self):
        print("Add Button %d" % self.line_count)
        x = [x for x in range(0, 100)]
        y = [random.randint(0, 100) for x in range(0, 100)]
        title = "Line #%d" % self.line_count
        self.mpl.addLine(x, y, title)
        self.line_count += 1
        return

    def updateRemoveButton(self):
        print("Remove Button %d" % self.line_count)
        self.line_count -= 1
        self.mpl.removeLine(self.line_count)
        return
