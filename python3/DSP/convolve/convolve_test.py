#! /usr/bin/env python3

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import sys
sys.path.append('../Signal')
import Signal

if __name__ == "__main__":
    width = 3
    time_array = np.linspace(-np.pi*width, np.pi*width, 128*width)
    wave1 = Signal.Signal(time_array, 2, 5, 0)
    wave1.calculateSineWave()
    window = signal.hamming(len(wave1.getSineWave))

    conv = signal.convolve(wave1.getSineWave, window)
    conv_len = len(conv)

    print("Len Wave1 {}".format(len(wave1.getSineWave)))
    print("Len Conv {}".format(len(conv)))

    plt.figure(1)

    plt.subplot(311)
    plt.grid(True)
    plt.plot(time_array, wave1.getSineWave)

    plt.subplot(312)
    plt.grid(True)
    plt.plot(time_array, window)

    plt.subplot(313)
    plt.grid(True)
    plt.plot(time_array, conv[0:(conv_len/2)+1])

    plt.show()
