'''
Created on Mar 18, 2013

@author: tractp1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class SmartPopUp(QDialog):

    def __init__(self, name="", count=0, parent=None):
        super(SmartPopUp, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.count = count
        self.name = name

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply |
                                     QDialogButtonBox.Cancel)

        self.connect(buttonBox.button(QDialogButtonBox.Apply),
                     SIGNAL("clicked()"), SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))

        self.Label = QLabel("Smart Pop up %s: %d" % (self.name, self.count))

        top_layout = QVBoxLayout()
        self.setLayout(top_layout)
        top_layout.addWidget(self.Label)
        top_layout.addWidget(buttonBox)
        self.setWindowTitle("Smarter Pop Up")

        return


class PopUp (QDialog):

    def __init__(self, parent=None):
        super(PopUp, self).__init__(parent)

        widthLabel = QLabel("&Width:")
        self.widthComboBox = QComboBox()
        widthLabel.setBuddy(self.widthComboBox)
        lst = [str(x) for x in range(24)]
        self.widthComboBox.addItems(lst)

        #######################################################################
        #
        # Buttons
        #
        #######################################################################
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)
        self.connect(buttonBox, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.widthComboBox)
        top_layout.addWidget(buttonBox)
        self.setLayout(top_layout)

        self.setWindowTitle("Pop Up")
        return


class UI(QDialog):

    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(UI, self).__init__(parent)

        #######################################################################
        #
        # DATE Editor
        #
        #######################################################################
        self.StartDateLabel = QLabel()
        self.EndDateLabel = QLabel()

        self.StartDate = QDateEdit()
        self.StartDate.setCalendarPopup(True)
        self.EndDate = QDateEdit(QDate.currentDate())
        self.EndDate.setCalendarPopup(True)

        self.StartDateLabel.setText("Start %s" % self.StartDate.date().toString("yyyy-MM-dd"))
        self.EndDateLabel.setText("End %s" % self.EndDate.date().toString("yyyy-MM-dd"))

        top_layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.StartDateLabel)
        left_layout.addWidget(self.EndDateLabel)
        right_layout.addWidget(self.StartDate)
        right_layout.addWidget(self.EndDate)

        date_layout.addLayout(left_layout)
        date_layout.addLayout(right_layout)

        #######################################################################
        #
        # Dial
        #
        #######################################################################
        self.Dial = QDial()
        self.Dial.setValue(0)
        self.Dial.setMaximum(1024)
        self.DialLabel = QLabel("Dial %d" % self.Dial.value())

        dial_layout = QHBoxLayout()
        dial_left_layout = QVBoxLayout()
        dial_right_layout = QVBoxLayout()

        dial_left_layout.addWidget(self.DialLabel)
        dial_right_layout.addWidget(self.Dial)
        dial_layout.addLayout(dial_left_layout)
        dial_layout.addLayout(dial_right_layout)

        # Connect signals to make things happen
        self.connect(self.Dial, SIGNAL("valueChanged(int)"), self.updateDial)

        #######################################################################
        #
        # Time, Timer, Time Editor
        #
        #######################################################################
        print("%s" % QTime.currentTime().toString("hh:mm:ss"))
        self.TimeLabel = QLabel("Time:")
        self.TimeValue = QLabel("%s" % QTime.currentTime().toString("hh:mm:ss"))
        self.Timer = QTimer()
        self.Timer.setSingleShot(False)
        self.Timer.start(1000)

        time_layout = QHBoxLayout()
        time_left_layout = QVBoxLayout()
        time_right_layout = QVBoxLayout()
        time_left_layout.addWidget(self.TimeLabel)
        time_right_layout.addWidget(self.TimeValue)
        time_layout.addLayout(time_left_layout)
        time_layout.addLayout(time_right_layout)

        self.connect(self.Timer, SIGNAL("timeout()"), self.updateTime)

        #######################################################################
        #
        # Buttons
        #
        #######################################################################
        self.Button1Count = 0
        self.Button2Count = 0

        self.Button1 = QPushButton("Test Button 1: Count %d" % self.Button1Count)
        self.Button2 = QPushButton("Test Button 2: Count %d" % self.Button2Count)

        button_layout = QHBoxLayout()
        button_left_layout = QVBoxLayout()
        button_right_layout = QVBoxLayout()
        button_left_layout.addWidget(self.Button1)
        button_right_layout.addWidget(self.Button2)
        button_layout.addLayout(button_left_layout)
        button_layout.addLayout(button_right_layout)

        self.connect(self.Button1, SIGNAL("clicked()"), self.updateButton1)
        self.connect(self.Button2, SIGNAL("clicked()"), self.updateButton2)

        #######################################################################
        #
        # Slider
        #
        #######################################################################
        self.SliderValue = QSlider()
        self.SliderLabel = QLabel("Slider %d" % self.SliderValue.value())

        slider_layout = QHBoxLayout()
        slider_left_layout = QVBoxLayout()
        slider_right_layout = QVBoxLayout()
        slider_left_layout.addWidget(self.SliderLabel)
        slider_right_layout.addWidget(self.SliderValue)
        slider_layout.addLayout(slider_left_layout)
        slider_layout.addLayout(slider_right_layout)

        self.connect(self.SliderValue, SIGNAL("valueChanged(int)"), self.updateSlider)

        #######################################################################
        #
        # LCD
        #
        #######################################################################
        self.LCDLabel = QLabel("LCD")
        self.LCDNumber = QLCDNumber()
        self.LCDNumber.setHexMode()
        self.LCDNumber.setNumDigits(4)
        self.LCDNumber.display(0000)

        p = QPalette()
        p.setColor(self.LCDNumber.backgroundRole(), Qt.red)
        self.LCDNumber.setAutoFillBackground(True)
        self.LCDNumber.setPalette(p)

#        np = QPalette()
#        np.setColor(np.windowText(),Qt.red)
#        self.LCDLabel.setPalette(np);

        lcd_layout = QHBoxLayout()
        lcd_left_layout = QVBoxLayout()
        lcd_right_layout = QVBoxLayout()
        lcd_left_layout.addWidget(self.LCDLabel)
        lcd_right_layout.addWidget(self.LCDNumber)
        lcd_layout.addLayout(lcd_left_layout)
        lcd_layout.addLayout(lcd_right_layout)

        #######################################################################
        #
        # Radio Buttons
        #
        #######################################################################
        # groupBox = QGroupBox("Exclusive Radio Buttons")

        self.radio1 = QRadioButton("&Radio button 1")
        self.radio2 = QRadioButton("R&adio button 2")
        self.radio3 = QRadioButton("Ra&dio button 3")
        self.RadioLabel = QLabel("Button Clicked")

        self.radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(self.radio3)
        vbox.addWidget(self.RadioLabel)
        vbox.addStretch(1)
        # groupBox.setLayout(vbox)

        self.connect(self.radio1, SIGNAL("clicked(bool)"), self.updateRadio1)
        self.connect(self.radio2, SIGNAL("clicked(bool)"), self.updateRadio2)
        self.connect(self.radio3, SIGNAL("clicked(bool)"), self.updateRadio3)

        #######################################################################
        #
        # Combo Box
        #
        #######################################################################
        self.ComboBoxLabel = QLabel("Combo Box Label")
        self.ComboBox = QComboBox()

        items = ["First", "Second", "Third"]
        self.ComboBox.addItems(items)
        combobox_layout = QHBoxLayout()
        combobox_left_layout = QVBoxLayout()
        combobox_right_layout = QVBoxLayout()
        combobox_left_layout.addWidget(self.ComboBoxLabel)
        combobox_right_layout.addWidget(self.ComboBox)
        combobox_layout.addLayout(combobox_left_layout)
        combobox_layout.addLayout(combobox_right_layout)
        self.connect(self.ComboBox, SIGNAL("currentIndexChanged (int)"), self.updateComBoBox)

        #######################################################################
        #
        # Top Level Display
        #
        #######################################################################
        top_layout.addLayout(date_layout)
        top_layout.addLayout(dial_layout)
        top_layout.addLayout(time_layout)
        top_layout.addLayout(button_layout)
        top_layout.addLayout(slider_layout)
        top_layout.addLayout(lcd_layout)
        top_layout.addLayout(vbox)
        top_layout.addLayout(combobox_layout)
        self.setLayout(top_layout)

        self.setWindowTitle("GUI TESTING")

        return

    def updateTime(self):
        self.TimeValue.setText("%s" % QTime.currentTime().toString("hh:mm:ss"))
        self.LCDNumber.display(self.LCDNumber.value() + 1)
        return

    def updateDial(self):
        self.DialLabel.setText("Dial %d" % self.Dial.value())

        smart = SmartPopUp("Dial", self.Dial.value())
        if smart.exec_():
            print("Applied")
        else:
            print("Canceled")

        return

    def updateButton1(self):
        self.Button1Count = self.Button1Count + 1
        self.Button1.setText("Test Button 1: Count %d" % self.Button1Count)
        pop = PopUp()
        if pop.exec_():
            print("%s" % (pop.widthComboBox.currentText()))
        else:
            print("Canceled!")
        return

    def updateButton2(self):
        self.Button2Count = self.Button2Count + 1
        self.Button2.setText("Test Button 2: Count %d" % self.Button2Count)
        return

    def updateSlider(self):
        self.SliderLabel.setText("Slider %d" % self.SliderValue.value())

        smart = SmartPopUp("Slider", self.SliderValue.value())
        if smart.exec_():
            print("Applied")
        else:
            print("Canceled")

        return

    def updateStartDate(self):
        self.StartDateLabel.setText("Start %s" % self.StartDate.date().toString("yyyy-MM-dd"))
        return

    def updateEndDate(self):
        self.EndDateLabel.setText("End %s" % self.EndDate.date().toString("yyyy-MM-dd"))
        return

    def updateRadio1(self):
        self.RadioLabel.setText("Radio 1 Clicked")
        return

    def updateRadio2(self):
        self.RadioLabel.setText("Radio 2 Clicked")
        return

    def updateRadio3(self):
        self.RadioLabel.setText("Radio 3 Clicked")
        return

    def updateComBoBox(self):
        self.ComboBoxLabel.setText(self.ComboBox.currentText())
        return

if __name__ == '__main__':
    print("Wrong Window!")
