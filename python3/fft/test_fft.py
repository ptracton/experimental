#! /usr/bin/env python3

import numpy as np


if __name__ == "__main__":
    data = [0xAAAA for i in range(1024)];
    fft_results = np.fft.fft(data, n=64)
    print(fft_results)
