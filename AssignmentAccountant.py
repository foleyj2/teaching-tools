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
import re

class AssignmentAccountant():
    def __init__(self,infd):
        for line in infd:
            line = line.strip().rstrip()
            #print(f"line: '{line}'")
            # detect grading comment
            # at least 2 capital letters possibly followed by a number and/or exclamation,
            # then sometimes (CODE), sometimes with a colon
            detect_grade_re = re.compile(r'(^[A-Z]{2,}\d?\!?)(\(\S+\))?\:?(.*)')
            checkedline = detect_grade_re.match(line)
            if checkedline:
                print(f"CODE: {checkedline.group(1)} OPTVAL: {checkedline.group(2)} COMMENT: {checkedline.group(3)}")

    def dump_values(self,outfd):
        '''Given a file descriptor, iterate line by line and parse comments'''
        pass

def main():
    """Main program loop"""
    print("""Assignment Accountant by Joseph. T. Foley<foley AT ru DOT is>
    From https://github.com/foleyj2/teaching-tools""")
    parser = argparse.ArgumentParser(
        description="Process Comments into Assignment values.")
    parser.add_argument('filepaths', nargs=argparse.REMAINDER)
    parser.add_argument('--log', default="INFO",
        help='Log level:  Number or DEBUG, INFO, WARNING, ERROR')
    parser.add_argument('--ext', default=".act",
                        help='Extension for output')

    args = parser.parse_args()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    datestring = 'AssignmentAccountant-{:%Y%m%d-%H%M%S}.log'.format(datetime.now())
    logging.basicConfig(format='%(message)s',
                        filename=datestring, level=numeric_level)
    logging.info("Creating AsignmentAccountant log file %s", datestring)

    for filepath in args.filepaths:
      # filename pre-processing for output
      inpath = PurePath(filepath)
      outpath = inpath.with_suffix(args.ext)
      print(f"File: {inpath} -> {outpath}")
      with open(outpath, "w") as outfd, open(inpath) as infd:
          AA = AssignmentAccountant(infd)
          AA.dump_values(outfd)
if __name__ == "__main__":
  main()
