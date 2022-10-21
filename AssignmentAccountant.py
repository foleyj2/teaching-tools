#!/usr/bin/python3
## Assignment credit/penalty calculations
##   typically from a text file or PdfAnnotations dump
## By Joseph T. Foley <foley AT RU.IS>
## Created 2022-09-14
import os
from pathlib import PurePath##https://docs.python.org/3/library/pathlib.html#module-pathlib
import argparse
import logging
from datetime import datetime
from decimal import *
import re

class AssignmentAccountant():
    Ledger = dict()
    def __init__(self, infd, logger):
        self.logger = logger
        detect_grade_re = re.compile(r'(^[A-Z]{2,}\d?\!?)(\(\S+\))?\:?(.*)')
        strip_outer_parens_re = re.compile(r'\((.*)\)')
        for line in infd:
            maybelines = line.strip().rstrip()
            for line in maybelines.splitlines():# in case it is a multiline comment
            #print(f"line: '{line}'")
            # detect grading comment
            # at least 2 capital letters possibly followed by a number and/or exclamation,
            # then sometimes (CODE), sometimes with a colon
                
                checkedline = detect_grade_re.match(line)
                if checkedline:
                    code, optval, comment = checkedline.groups()
                    if optval:
                        optval_match = strip_outer_parens_re.match(optval)
                        if optval_match:
                            optval = optval_match.group(1)
                            
                    logger.warning(f"CODE: {code} OPTVAL: {optval} COMMENT: {comment}")
                    self.parse_values(code, optval, comment)
    def parse_values(self, code, optval, comment, always_inc=True):
        """Take comment and turn into operations on ledger"""
        logger = self.logger
        # examine code first
        # STUB:  Just use as is
        keycode = code
        # got a key, time to update value
        keyval = self.Ledger.setdefault(keycode, 0)
        # if there's a string in there, don't mess with it
        if isinstance(keyval, str):
            return
        def updateentry(keyval, increment=None):
            if always_inc: # increment even if negative
                increment = abs(increment)
            if increment:
                self.Ledger[keycode] = keyval + increment
            else:
                self.Ledger[keycode] = keyval
            self.logger.info(f"keycode:{keycode} keyval:{keyval}, increment:{increment}")
        
        # what is going on with opval?
        increment = 0
        if optval is None:
            increment = 1
        elif isinstance(optval,int):
            increment = Decimal(optval)
        elif isinstance(optval, str):
            try:
                x = float(optval)
                increment = Decimal(optval)
                updateentry(keyval, increment)
                return
            except ValueError:
                pass # not a valid number

            if optval.startswith('='): # Force value
                optval = optval.removeprefix('=')
                increment = 0
                keyval = Decimal(optval)
            else:
                # might be string command
                keyval = optval
                increment = 0
        
        else:
            logger.error(f"Unknown value/command:  '{optval}' of type {type(optval)}")
        updateentry(keyval, increment)
                
    def dump_values(self,outfd):
        '''Given a file descriptor, iterate line by line output the database'''
        keyvals = sorted(self.Ledger.items())
        for (key, val) in keyvals:
            print(f"{key} {val}", file=outfd)

def main():
    """Main program loop"""
    print("""Assignment Accountant by Joseph. T. Foley<foley AT ru DOT is>
    From https://github.com/foleyj2/teaching-tools""")
    parser = argparse.ArgumentParser(
        description="Process Comments into Assignment values.")
    parser.add_argument('filepaths', nargs=argparse.REMAINDER)
    ## TODO:  Fix verbosity based upon another argument and logging
    parser.add_argument('--log', default="INFO",
        help='Console log level:  Number or DEBUG, INFO, WARNING, ERROR')
    parser.add_argument('--ext', default=".act",
                        help='Extension for output')

    args = parser.parse_args()
    ## Set up logging
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    print(f"Log level:  {numeric_level}")
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    # log everything to file
    logpath = 'AssignmentAccountant-{:%Y%m%d-%H%M%S}.log'.format(datetime.now())
    fh = logging.FileHandler(logpath)
    fh.setLevel(logging.DEBUG)
    # log to console
    ch = logging.StreamHandler()
    ch.setLevel(numeric_level)
    # create formatter and add to handlers
    consoleformatter = logging.Formatter('%(message)s')
    ch.setFormatter(consoleformatter)
    spamformatter = logging.Formatter('%(asctime)s %(name)s[%(levelname)s] %(message)s')
    fh.setFormatter(spamformatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.info("Creating AssignmentAccountant log file %s", logpath)

    for filepath in args.filepaths:
      # filename pre-processing for output
      inpath = PurePath(filepath)
      outpath = inpath.with_suffix(args.ext)
      print(f"File: {inpath} -> {outpath}")
      input = None
      # Is this a PDF? If so, we need to extract the comments
      if inpath.suffix == ".pdf":
          import PdfAnnotations
          pdfannotations = PdfAnnotations.PdfAnnotations(inpath)
          input = pdfannotations.extract_comments()
      else:
          input = open(inpath)
      
      with open(outpath, "w") as outfd:
          AA = AssignmentAccountant(input,logger)
          AA.dump_values(outfd)
if __name__ == "__main__":
  main()
