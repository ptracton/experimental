'''
Created on Mar 18, 2013

@author: tractp1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class InterestUI(QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor            
        '''

        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(InterestUI, self).__init__(parent)

        #
        # Create the various GUI objects needed for display
        #
        self.PrincipleLabel = QLabel("Principle")
        self.PrincipleDoubleSpinBox = QDoubleSpinBox()
        self.PrincipleDoubleSpinBox.setRange(0, 100000000);
        self.PrincipleDoubleSpinBox.setSingleStep(100);
        self.PrincipleDoubleSpinBox.setValue(2000.00);
        self.PrincipleDoubleSpinBox.setPrefix("$ ")

        self.RateLabel = QLabel("Rate")
        self.RateDoubleSpinBox = QDoubleSpinBox()
        self.RateDoubleSpinBox.setRange(0, 10);
        self.RateDoubleSpinBox.setSingleStep(0.25);
        self.RateDoubleSpinBox.setValue(1.00);
        self.RateDoubleSpinBox.setSuffix("%")

        self.YearsLabel = QLabel("Years")
        self.YearsComboBox = QComboBox()
        strList = [str(x) + (" Years") for x in range(1, 101)]
        print (strList)
        self.YearsComboBox.addItems(strList)

        self.AmountLabel = QLabel("Amount")
        self.AmountValueLabel = QLabel("$ 0.00")

        #
        # Grid is just a local variable not an object (self) variable
        # Once the layout is done, we do NOT change it
        #
        grid = QGridLayout()
        grid.addWidget(self.PrincipleLabel, 0, 0)
        grid.addWidget(self.RateLabel, 1, 0)
        grid.addWidget(self.YearsLabel, 2, 0)
        grid.addWidget(self.AmountLabel, 3, 0)

        grid.addWidget(self.PrincipleDoubleSpinBox, 0, 1)
        grid.addWidget(self.RateDoubleSpinBox, 1, 1)
        grid.addWidget(self.YearsComboBox, 2, 1)
        grid.addWidget(self.AmountValueLabel, 3, 1)
        self.setLayout(grid)

        #
        # Connect signals to make things happen
        #
        self.connect(self.YearsComboBox,
                     SIGNAL("currentIndexChanged(int)"), self.updateUI)
        self.connect(self.RateDoubleSpinBox,
                     SIGNAL("valueChanged(double)"), self.updateUI)
        self.connect(self.PrincipleDoubleSpinBox,
                     SIGNAL("valueChanged(double)"), self.updateUI)

        self.setWindowTitle("Interest")

    def updateUI(self):
        years = int((self.YearsComboBox.currentText()).strip(" Years"))
        principle = self.PrincipleDoubleSpinBox.value()
        rate = self.RateDoubleSpinBox.value()
        amount = 0
        amount = principle * ((1 + (rate / 100.0)) ** years)
        self.AmountValueLabel.setText("$ %0.2f" % amount)
        print("UPDATING UI: years = %s principle = %s rate = %s, amount = %f" % (years, principle, rate, amount))
        return
