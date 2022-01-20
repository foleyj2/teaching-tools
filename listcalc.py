#!/usr/bin/env python3
# quick calculating of means of lists of numbers
from decimal import Decimal, ROUND_HALF_UP
import sys
import decimal
import argparse
from datetime import datetime
import logging


def main():
    """Main program loop"""
    print("""Mean list calculator by Joseph. T. Foley<foley AT ru DOT is>
    From https://github.com/foleyj2/teaching-tools""")
    parser = argparse.ArgumentParser(
        description="Do some repeated calculations on lists of numbers.")
    parser.add_argument('--stoplen', dest='stoplen', type=int,
                        help='Stop calculation after N values.')
    parser.add_argument('--maxval', type=Decimal,
                        help='Max value for each grading element.')
    parser.add_argument('--log', default="INFO",
        help='Log level:  Number or DEBUG, INFO, WARNING, ERROR')
    args = parser.parse_args()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    datestring = 'listcalc-{:%Y%m%d-%H%M%S}.log'.format(datetime.now())
    logging.basicConfig(format='%(message)s',
                        filename=datestring, level=numeric_level)
    logging.info("Creating Listcalc log file %s", datestring)


    calc = Listcalc(stoplen=args.stoplen, maxval=args.maxval)
    while True:
        calc.getvals()
        calc.mean()
        calc.reset()


class Listcalc():
    """Get a list of values from somewhere and do something useful."""
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
            myscore = mysum/mybase
            myscore_rounded = myscore.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            percentage = 100*myscore
            percentage_rounded = percentage.quantize(Decimal('.1'), rounding=ROUND_HALF_UP)
            tengrade = 10*myscore
            tengrade_rounded = tengrade.quantize(Decimal('.1'), rounding=ROUND_HALF_UP)
            tengrade = Decimal(10*myscore.quantize(Decimal('.01'),
                                                  rounding=ROUND_HALF_UP))
            displayval = f"{val_log} => {mysum}/{mybase} = {myscore_rounded} =  {percentage_rounded}% ~ {tengrade_rounded}/10"
            print(displayval)
            logging.info(displayval)
        else:  # normal case:  straight average
            mymean = mysum/mybase
            output = Decimal(mymean.quantize(Decimal('.1'),
                                             rounding=ROUND_HALF_UP))
            displayval = f"{val_log} => {mysum}/{mybase} = {output}"
            print(displayval)
            logging.info(displayval)
        # for grading purpose, students want more information

    def reset(self):
        """Clear the values"""
        self.accum = []

    def getval(self, src="kbd"):
        """Get a value from somewhere and put it in the accumulator"""
        if src == "kbd":
            currentindex = len(self.accum)+1 #humans like indexes to start at 1
            myinput = (input(f"val{currentindex}: "))
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
    main()
