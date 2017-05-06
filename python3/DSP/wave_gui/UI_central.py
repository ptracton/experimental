
from scipy import signal, fftpack
from PyQt4 import QtCore
from PyQt4 import QtGui
import SignalWaveAndConfig
import SignalWaveAndOperation


class UI_central(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(UI_central, self).__init__(parent)
        print("UI_central Starting")

        self.top_layout = QtGui.QVBoxLayout()
        self.waveform1 = SignalWaveAndConfig.SignalWaveAndConfig(parent)
        self.waveform2 = SignalWaveAndConfig.SignalWaveAndConfig(parent)
        self.operation = SignalWaveAndOperation.SignalWaveAndOperation(parent)
        
        self.top_layout.addLayout(self.waveform1.getLayout())
        self.top_layout.addLayout(self.waveform2.getLayout())
        self.top_layout.addLayout(self.operation.getLayout())

        self.connect(self.operation.signalOperation.executeButton,
                     QtCore.SIGNAL("clicked()"),
                     self.executeButtonClicked)
        
        self.setLayout(self.top_layout)
        return

    def executeButtonClicked(self):
        print("Execute Button Clicked")
        operation = self.operation.signalOperation.operations.entry.currentText()
        print("Operation {}".format(operation))

        waveform1 = self.waveform1.signalConfig.waveform.entry.currentText()
        waveform2 = self.waveform2.signalConfig.waveform.entry.currentText()
        print("Waveform1 {}".format(waveform1))
        print("Waveform2 {}".format(waveform2))

        data1 = []
        if waveform1 == "Sine":
            data1 = self.waveform1.Signal.getSineWave
        elif waveform1 == "Cosine":
            data1 = self.waveform1.Signal.getCosineWave
        elif waveform1 == "Square":
            data1 = self.waveform1.Signal.getSquareWave
        elif waveform1 == "Sawtooth":
            data1 = self.waveform1.Signal.getSawtoothWave
        else:
            data1 = []

        data2 = []
        if waveform2 == "Sine":
            data2 = self.waveform2.Signal.getSineWave
        elif waveform2 == "Cosine":
            data2 = self.waveform2.Signal.getCosineWave
        elif waveform2 == "Square":
            data2 = self.waveform2.Signal.getSquareWave
        elif waveform2 == "Sawtooth":
            data2 = self.waveform2.Signal.getSawtoothWave
        else:
            data2 = []
            
        results = []
        if operation == "ADD":
            results = data1 + data2
        elif operation == "SUB":
            results = data1 - data2
        elif operation == "MULT":
            results = data1 * data2
        elif operation == "CONV":
            full_results = signal.convolve(data1, data2)
            length = len(full_results)
            results = full_results[0:(length/2)+1]
        elif operation == "FFT":
            results = fftpack.fft(data1)
        else:
            results = []
            
        if results is not []:
            self.operation.mplGraph.removeLine()
            self.operation.mplGraph.addLine(self.waveform1.Signal.sample_times,
                                            results, operation)
            
        return
