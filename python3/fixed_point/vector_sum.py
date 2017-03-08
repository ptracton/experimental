#! /usr/bin/env python3

import argparse
import decimal

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Vector Sum')
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
    
    args = parser.parse_args()
    if args.debug:
        print(args)

    x = decimal.Decimal(0x1234)
    print ('0x%x' % x)
    print (x.max(32767))
    print (x.min(-32768))
    print (x.is_signed())
    print (x + 0x7FF0)
    
