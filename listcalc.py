#!/usr/bin/env python3
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
    def __init__(self,stoplen=None,maxval=None):
        #dcontext = decimal.getcontext()
        #dcontext.prec = 3
        #dcontext.flags[decimal.Rounded]
        self.stoplen = stoplen
        self.maxval = maxval
    def append(self,val):
        """put another value on"""
        try:
            self.accum.append(Decimal(val))
        except decimal.InvalidOperation:
            raise ValueError
    def mean(self):
        """Calculate the mean of the current values"""
        mysum = Decimal(sum(self.accum))
        mybase = len(self.accum)
        if mybase < 1:
            print("mean: infinite")
            return
        
        # normal case:  straight average
        if self.maxval:
            mybase = mybase * self.maxval
            # grading points case:  total divided by maximum
            
        mymean = mysum/mybase
        output = Decimal(mymean.quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
        print(f"mean: {mysum}/{mybase} = {output}")
            

    def reset(self):
        """Clear the values"""
        self.accum = []
    def getval(self,src="kbd"):
        """Get a value from somewhere and put it in the accumulator"""
        retval = None
        if src == "kbd":
            myinput = (input("val: "))
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
    print("Mean list calculator by Joseph. T. Foley<foley AT ru DOT is>")
    parser = argparse.ArgumentParser(description="Do some repeated calculations on lists of numbers.")
    parser.add_argument('--stoplen', dest='stoplen', type=int,
                        help='Stop calculation after N values.')
    parser.add_argument('--maxval', type=Decimal,
                        help='Max value for each grade.')

    args = parser.parse_args()
    calc = Listcalc(stoplen=args.stoplen, maxval=args.maxval)
    while True:
        calc.getvals()
        calc.mean()
        calc.reset()
