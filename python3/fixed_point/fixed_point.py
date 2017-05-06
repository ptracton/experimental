#! /usr/bin/env python3

import decimal



    
if __name__ == "__main__":
    print("Fixed Point")
    decimal.getcontext().prec = 1
    decimal.getcontext().Emax = 32767
    decimal.getcontext().Emin = -32768
    x = decimal.Decimal(0x8f61)
    y = decimal.Decimal(0x0324)
    z = x * y
    print (decimal.getcontext())
    print (x.as_tuple())
    print (y.as_tuple())
    print (z.as_tuple())
