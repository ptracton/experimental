#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot
import numpy
import HSR

if __name__ == "__main__":
    print ("Test HSR")

    parser = argparse.ArgumentParser(
        description='Testing HSR Math')
    parser.add_argument("-D", "--debug",
                        help="Debug this script",
                        action="store_true")
    parser.add_argument("--waveform1",
                        help="First Waveform",
                        required=False,
                        default=None,
                        action="store")
    parser.add_argument("--waveform2",
                        help="Second Waveform",
                        required=False,
                        default=None,
                        action="store")
    parser.add_argument("--plot",
                        help="Plot Waveforms and Results",
                        required=False,
                        default=-1,
                        action="store_true")
   

    args = parser.parse_args()
    if args.debug:
        print(args)    
    
    foo = HSR.VectorSum.VectorSum()
    foo.vector1.file_name = 'waveforms/rail2railnegramp.txt'
    foo.vector2.file_name = 'waveforms/sine_1hz.txt'
    foo.result_vector.file_name = 'vsum_maxrate_sine_1hz.txt'
    foo.vector1.read_vector()
    foo.vector2.read_vector()
    foo.r_scale = 5
    foo.calculate()
    foo.vector1.store_vector()
    foo.vector2.store_vector()
    foo.result_vector.store_vector()
    if args.plot:
        X = numpy.linspace(0, foo.vector1.size, foo.vector1.size, endpoint=True)

        ax1 = matplotlib.pyplot.subplot(311)
        matplotlib.pyplot.plot(X, foo.vector1.vector)
        matplotlib.pyplot.setp(ax1.get_xticklabels(), fontsize=6)
        ax1_title = "%s" % foo.vector1.file_name_root
        ax1.set_title(ax1_title)
        axes = matplotlib.pyplot.gca()
       # axes.get_xaxis().set_major_locator(matplotlib.ticker.MultipleLocator(1))
        axes.get_xaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%x"))
        
        ax2 = matplotlib.pyplot.subplot(312, sharex=ax1, sharey=ax1)
        matplotlib.pyplot.plot(X, foo.vector2.vector)
        matplotlib.pyplot.setp(ax2.get_xticklabels(), fontsize=6)
        ax2_title = "%s" % foo.vector2.file_name_root
        
        ax3 = matplotlib.pyplot.subplot(313, sharex=ax1, sharey=ax1)
        matplotlib.pyplot.plot(X, foo.result_vector.vector)
        matplotlib.pyplot.setp(ax3.get_xticklabels(), fontsize=6)
        
        #matplotlib.pyplot.plot(X, foo.vector1.vector)
       # matplotlib.pyplot.plot(X, foo.vector2.vector)
        #matplotlib.pyplot.plot(X, foo.result_vector.vector)
        plot_title = "Vector Sum %s and %s with R_Scale = 0x%08x" % (foo.vector1.file_name_root, foo.vector2.file_name_root, foo.r_scale)
        matplotlib.pyplot.title(plot_title)
        matplotlib.pyplot.show()
