#!/usr/bin/env python3

import sys


import PyQt5
import PyQt5.QtCore
import PyQt5.QtWidgets

import numpy as np
import pyqtgraph as pg


class UI_Widget(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UI_Widget, self).__init__(parent)
        vbox = PyQt5.QtWidgets.QVBoxLayout()

        #pg.setConfigOption('background', 'b')
        #pg.setConfigOption('foreground', 'w')

        my_plot = pg.PlotWidget()
        vbox.addWidget(my_plot)
        my_plot.setWindowTitle("Graph Title")
        my_plot.addLegend((100,60), offset=(70,30))
        my_plot.plot(np.random.normal(size=100), pen='r', name="Plot 1")
        my_plot.plot(np.random.normal(size=100), pen='g', name="Plot 2")
        my_plot.setLabel(axis='left', text='Y Axis', units='y units')
        my_plot.setLabel(axis='bottom', text='x Axis', units='x units')
        my_plot.showGrid(x=True, y=True)
        self.setLayout(vbox)
        return


class UI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        self.statusBar().showMessage('Menu Bar')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        exitAction = PyQt5.QtWidgets.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(PyQt5.QtWidgets.qApp.quit)
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.central = UI_Widget()

        self.setCentralWidget(self.central)
        self.setWindowTitle('Statusbar')
        self.show()

        return


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = UI()
    gui.show()
    app.exec_()
