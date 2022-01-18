#!/usr/bin/python
# quick calculating of means of lists of numbers
from decimal import Decimal, ROUND_HALF_UP
import sys
import decimal
import argparse

# getcontext().prec = 2
values = []
class Listcalc(object):
    """Take a list of values and do something useful."""
    accum = []
    stoplen = None
    def __init__(self,stoplen=None):
        #dcontext = decimal.getcontext()
        #dcontext.prec = 3
        #dcontext.flags[decimal.Rounded]
        self.stoplen = stoplen
    def append(self,val):
        """put another value on"""
        try:
            self.accum.append(Decimal(val))
        except decimal.InvalidOperation:
            raise ValueError
    def mean(self):
        """Calculate the mean of the current values"""
        mysum = Decimal(sum(self.accum))
        mylen = len(self.accum)
        if mylen < 1:
            print "mean: infinite"
            return
        mymean = mysum/mylen
        output = Decimal(mymean.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
        print "mean: %s/%s = %s" % (mysum, mylen, output)
    def reset(self):
        """Clear the values"""
        self.accum = []
    def getval(self,src="kbd"):
        """Get a value from somewhere and put it in the accumulator"""
        retval = None
        if src == "kbd":
            myinput = (raw_input("val: "))
            if myinput in ("x","X","q","Q","quit"):
                sys.exit("Quit!")
        else:
            myinput = src
        retval = self.append(myinput)
    def getvals(self,src="kbd"):
        """Get a value from somewhere until there is a NAN
           if a limit is set, then stop calculating when we
           hit that length"""
        try:
            while True:
                #print "%d vs %d" % (len(self.accum), self.stoplen)
                if self.stoplen and len(self.accum) >= self.stoplen:
                    return
                calc.getval(src=src)
        except ValueError:
            pass

if __name__ == '__main__':  #Main invocation
    print "Mean list calculator by Joseph. T. Foley<foley AT ru DOT is>"
    print "$Id: listcalc.py 1126 2017-11-14 23:11:45Z foley $"
    parser = argparse.ArgumentParser(description="Do some repeated calculations on lists of numbers.")
    parser.add_argument('--stoplen', dest='stoplen', type=int,
                        help='Stop calculation after N values.')
    args = parser.parse_args()
    calc = Listcalc(stoplen=args.stoplen)
    while True:
        calc.getvals()
        calc.mean()
        calc.reset()
