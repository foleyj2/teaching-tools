#!/usr/bin/env python3
# quick calculating of means of lists of numbers
from decimal import Decimal, ROUND_HALF_UP
import sys
import decimal
import argparse


class Listcalc():
    """Take a list of values and do something useful."""
    accum = []
    stoplen = None

    def __init__(self, stoplen=None, maxval=None):
        # dcontext = decimal.getcontext()
        # dcontext.prec = 3
        # dcontext.flags[decimal.Rounded]
        self.stoplen = stoplen
        self.maxval = maxval

    def append(self, val):
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
        val_log = "+".join([str(val) for val in self.accum])

        if self.maxval:  # grading points case:  total divided by maximum
            mybase = mybase*self.maxval
            mymean = mysum/mybase
            percentage = Decimal(100*mymean.quantize(Decimal('.1'),
                                                     rounding=ROUND_HALF_UP))
            tengrade = Decimal(10*mymean.quantize(Decimal('.1'),
                                                  rounding=ROUND_HALF_UP))
            print(f"{val_log} => {mysum}/{mybase} = {percentage}% ~ {tengrade}/10")
        else:  # normal case:  straight average
            mymean = mysum/mybase
            output = Decimal(mymean.quantize(Decimal('.1'),
                                             rounding=ROUND_HALF_UP))
            print(f"{val_log} => {mysum}/{mybase} = {output}")
        # for grading purpose, students want more information

    def reset(self):
        """Clear the values"""
        self.accum = []

    def getval(self, src="kbd"):
        """Get a value from somewhere and put it in the accumulator"""
        if src == "kbd":
            myinput = (input("val: "))
            if myinput in ("x", "X", "q", "Q", "quit"):
                sys.exit("Quit!")
        else:
            myinput = src
        self.append(myinput)

    def getvals(self, src="kbd"):
        """Get a value from somewhere until there is a NAN
           if a limit is set, then stop calculating when we
           hit that length"""
        try:
            while True:
                if self.stoplen and len(self.accum) >= self.stoplen:
                    return
                self.getval(src=src)
        except ValueError:
            pass


if __name__ == '__main__':  # Main invocation
    print("Mean list calculator by Joseph. T. Foley<foley AT ru DOT is>")
    PARSER = argparse.ArgumentParser(
        description="Do some repeated calculations on lists of numbers.")
    PARSER.add_argument('--stoplen', dest='stoplen', type=int,
                        help='Stop calculation after N values.')
    PARSER.add_argument('--maxval', type=Decimal,
                        help='Max value for each grading element.')

    ARGS = PARSER.parse_args()
    CALC = Listcalc(stoplen=ARGS.stoplen, maxval=ARGS.maxval)
    while True:
        CALC.getvals()
        CALC.mean()
        CALC.reset()
