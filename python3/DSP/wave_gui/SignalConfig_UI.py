#! /usr/bin/env python3

import numpy as np
from PyQt4 import QtGui
import LabelAndEntry
import LabelAndComboBox


class SignalConfig_UI(QtGui.QDialog):

    def __init__(self, parent=None):
        super(SignalConfig_UI, self).__init__(parent)

        self.top_vbox = QtGui.QVBoxLayout()
        
        self.sample_time_start = LabelAndEntry.LabelAndEntry(
            label="Sample Time Start", lineDefault=-np.pi)

        self.sample_time_stop = LabelAndEntry.LabelAndEntry(
            label="Sample Stop Start",  lineDefault=np.pi)

        self.number_of_samples = LabelAndEntry.LabelAndEntry(
            label="Number of Samples",  lineDefault=64)

        self.frequency = LabelAndEntry.LabelAndEntry(
            label="Frequency",  lineDefault=1)

        self.amplitude = LabelAndEntry.LabelAndEntry(
            label="Amplitude",  lineDefault=1)

        self.offset = LabelAndEntry.LabelAndEntry(
            label="Offset",  lineDefault=0)

        optionsList = ["Sine", "Cosine", "Square", "Sawtooth"]
        self.waveform = LabelAndComboBox.LabelAndComboBox(
            label="Wave Forms", optionsList=optionsList
        )

        self.displayButton = QtGui.QPushButton("Display")
        
        self.top_vbox.addLayout(self.sample_time_start.getLayout())
        self.top_vbox.addLayout(self.sample_time_stop.getLayout())
        self.top_vbox.addLayout(self.number_of_samples.getLayout())
        self.top_vbox.addLayout(self.frequency.getLayout())
        self.top_vbox.addLayout(self.amplitude.getLayout())
        self.top_vbox.addLayout(self.offset.getLayout())
        self.top_vbox.addLayout(self.waveform.getLayout())
        self.top_vbox.addWidget(self.displayButton)
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.top_vbox
