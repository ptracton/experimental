#! /usr/bin/env python3

import operator
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

import sys
sys.path.append('../Signal')
import Signal

if __name__ == "__main__":
    width = 3
    time_array = np.linspace(-np.pi*width, np.pi*width, 64*width)
    wave1 = Signal.Signal(time_array, 2, 5, 0)
    wave2 = Signal.Signal(time_array, 10, 1, 0)
    wave1.calculateSineWave()
    wave2.calculateSquareWave()
    added = wave1.getSineWave + wave2.getSquareWave

    fft = fftpack.fft(added, 64*width)
    print("FFT Results {}".format(fft))
    print("FFT Length {}".format(len(fft)))
    print("Time Array Length {}".format(len(time_array)))
    max_index, max_value = max(enumerate(fft), key=operator.itemgetter(1))
    print("FFT Max {}".format(max_value))
    print("FFT Max Index {}".format(max_index))

    plt.figure(1)

    plt.subplot(311)
    plt.grid(True)
    plt.plot(time_array, wave1.getSineWave)

    plt.subplot(312)
    plt.grid(True)
    plt.plot(time_array, wave2.getSquareWave)

    plt.subplot(313)
    plt.grid(True)
    plt.plot(time_array, fft)

    plt.show()
