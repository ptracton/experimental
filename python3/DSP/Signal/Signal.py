#! /usr/bin/env python3

import numpy as np
from scipy import signal


class Signal():
    """
    The signal class handles creating and storing signals of various type for
    use in DSP applications
    """

    def __init__(self, sample_times=None, amplitude=1, frequency=1, offset=0):
        """
        sample_times is the dependant X axis variable.  usually time.
        amplitude is the scalar multiplier for scaling up or down the signal
        frequency is the scalar multiplier for the signal frequency
        offset is the scalar addition to the signal
        """
        self.sample_times = sample_times
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset
        self.sineWave = None
        self.cosineWave = None
        self.squareWave = None
        self.sawtoothWave = None
        return

    def calculateSineWave(self):
        self.sineWave = self.amplitude * np.sin((self.sample_times *
                                                 self.frequency) + self.offset)
        return

    def calculateCosineWave(self):
        self.cosineWave = self.amplitude * np.cos((
            self.sample_times * self.frequency) + self.offset)
        return

    def calculateSquareWave(self):
        self.squareWave = self.amplitude * signal.square((
            self.sample_times * self.frequency) + self.offset)

    def calculateSawtoothWave(self):
        self.sawtoothWave = self.amplitude * signal.sawtooth((
            self.sample_times * self.frequency) + self.offset)

    def calculateAll(self):
        self.calculateCosineWave()
        self.calculateSineWave()
        self.calculateSawtoothWave()
        self.calculateSquareWave()
        return

    @property
    def getSineWave(self):
        return self.sineWave

    @property
    def getCosineWave(self):
        return self.cosineWave

    @property
    def getSquareWave(self):
        return self.squareWave

    @property
    def getSawtoothWave(self):
        return self.sawtoothWave

    def __str__(self):
        string = "\nSample Times {}".format(self.sample_times)
        return string
