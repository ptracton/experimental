'''
Created on Apr 8, 2013

@author: tractp1
'''

from pprint import pprint
from PyQt4 import QtGui
import numpy as np
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg

class QtMpl(FigureCanvasQTAgg):
    '''
    '''
    def __init__(self, parent):

        self.fig = matplotlib.figure.Figure()

        FigureCanvasQTAgg.__init__(self, self.fig)

        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_ylabel("Y-Axis")
        self.axes.set_xlabel("X-Axis")
        self.line_list = []

        # we define the widget as expandable
        FigureCanvasQTAgg.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvasQTAgg.updateGeometry(self)

    def addLine(self, x, y, title):
        self.line_list.append(self.axes.plot(x, y, label = title))
        self.axes.legend()

        # http://stackoverflow.com/questions/4098131/matplotlib-update-a-plot
        self.fig.canvas.draw()
        return

    def removeLine(self, line_number):
        self.axes.lines.pop(0)
        self.axes.legend()
        self.fig.canvas.draw()
        return
