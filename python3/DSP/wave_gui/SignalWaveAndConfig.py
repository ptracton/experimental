#! /usr/bin/env python3

import numpy as np
from PyQt4 import QtCore
from PyQt4 import QtGui
import SignalConfig_UI
import QtMpl

import sys
sys.path.append('../Signal')
import Signal


class SignalWaveAndConfig(QtGui.QWidget):

    def __init__(self, parent=None, label="Default"):
        super(SignalWaveAndConfig, self).__init__(parent)
                
        self.top_hbox = QtGui.QHBoxLayout()

        self.signalConfig = SignalConfig_UI.SignalConfig_UI()
        self.mplGraph = QtMpl.QtMpl(parent)
        self.top_hbox.addLayout(self.signalConfig.getLayout())
        self.top_hbox.addWidget(self.mplGraph)

        self.Signal = Signal.Signal()
        
        self.connect(self.signalConfig.displayButton,
                     QtCore.SIGNAL("clicked()"),
                     self.displayButtonClicked)
        
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.top_hbox
    
    def displayButtonClicked(self):
        print("Display Button Clicked")

        start_time = self.signalConfig.sample_time_start.entry.text()
        if not start_time.isdecimal():
            start_time = -1 * np.pi
        print("Start Time {}".format(start_time))
        
        stop_time = self.signalConfig.sample_time_stop.entry.text()
        if not stop_time.isdecimal():
            stop_time = np.pi
        print("Stop Time {}".format(stop_time))

        number_of_samples = self.signalConfig.number_of_samples.entry.text()
        if not number_of_samples.isdecimal():
            number_of_samples = 64
        print("Number Of Samples {}".format(number_of_samples))

        frequency = self.signalConfig.frequency.entry.text()
        if not frequency.isdecimal():
            frequency = 1
        print("Frequency {}".format(frequency))

        amplitude = self.signalConfig.amplitude.entry.text()
        if not amplitude.isdecimal():
            amplitude = 1
        print("Amplitude {}".format(amplitude))

        offset = self.signalConfig.offset.entry.text()
        if not offset.isdecimal():
            offset = 1
        print("Offset {}".format(offset))

        waveform = self.signalConfig.waveform.entry.currentText()
        print("Waveform {}".format(waveform))

        self.Signal.amplitude = float(amplitude)
        self.Signal.frequency = float(frequency)
        self.Signal.offset = float(offset)
        self.Signal.sample_times = np.linspace(start_time, stop_time,
                                               int(number_of_samples))
        
        self.Signal.calculateAll()

        data = []
        if waveform == "Sine":
            data = self.Signal.getSineWave
        elif waveform == "Cosine":
            data = self.Signal.getCosineWave
        elif waveform == "Square":
            data = self.Signal.getSquareWave
        elif waveform == "Sawtooth":
            data = self.Signal.getSawtoothWave
        else:
            data = []

        if data is not []:
            self.mplGraph.removeLine()
            self.mplGraph.addLine(self.Signal.sample_times, data, waveform)
        return
