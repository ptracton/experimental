#! /usr/bin/env python3

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

if __name__ == "__main__":

    width = 5
    
    time_array = np.linspace(-np.pi*width, np.pi*width, 64*width)
    
    sawtooth = signal.sawtooth(time_array*5)
    square = signal.square(time_array*4)
    sine = 2*np.sin(time_array*3)
    cosine = np.cos(time_array*2)
    tangent = np.tan(time_array)
    
    plt.figure(1)
    
    plt.subplot(911)
    plt.grid(True)
    plt.stem(time_array, sawtooth)

    plt.subplot(912)
    plt.grid(True)
    plt.plot(time_array, sine)
    
    plt.subplot(913)
    plt.grid(True)
    plt.stem(time_array, sine, top=+5)

    plt.subplot(914)
    plt.grid(True)
    plt.stem(time_array, cosine,  bottom=-2)
    
    plt.subplot(915)
    plt.grid(True)
    plt.stem(time_array, square)

    plt.subplot(916)
    signal_sum = sawtooth + sine + cosine + square
    plt.grid(True)
    plt.stem(time_array, signal_sum)

    plt.subplot(917)
    signal_sum = sawtooth + sine + cosine + square
    plt.grid(True)
    plt.plot(time_array, signal_sum)

    plt.subplot(918)
    signal_mult = cosine * sine
    plt.grid(True)
    plt.stem(time_array, signal_mult)

    plt.subplot(919)
    plt.grid(True)
    plt.plot(time_array, signal_mult)

    

    plt.show()
    
