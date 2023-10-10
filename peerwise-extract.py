#!/usr/bin/python3
## Tool for extracting peerwise questions for making oral quizzes
## Author:  Joseph T. Foley <foley AT RU DOT IS>
## Start Date: 2023-10-10
## Input: CSV file from Peerwise course Main > Administration > Export all questions
##    Number of questions to export: All questions
##    Display questions in order: Student "identifiers
##    Format:  Text only, excluding layout and images
##    Additional Data:  Only the question author's content
## Output:  CSV with date, question, answer

import os
import pathlib
import argparse
import logging
from datetime import datetime
#from collections import OrderedDict
import re
import csv

class PeerwiseCSV():
    """Handle all Peerwise CSV operations."""
    def __init__(self, filepath, logger, outpath):
        self.logger = logger
        with open(filepath, newline="") as csvfile:            
            reader = csv.DictReader(csvfile)
            with open(outpath, "w", newline='') as outputfile:
                writer = csv.writer(outputfile)
                headings = ["timestamp", "question", "answer"]
                writer.writerow(headings)
                for row in reader:
                    answerid = row["answer"]
                    cols = [row["timestamp"], row["question"], row["option"+answerid]]
                    logger.debug(cols)
                    writer.writerow(cols)
                    

                
#    def dump_values(self,outfd):
#        '''Given a file descriptor, iterate line by line output the database'''
#        keyvals = sorted(self.codes.items())
#        for (key, val) in keyvals:
#            print(f"{key} {val}", file=outfd)
        
#    def get_codes(self):
#        return(self.codes)

def main():
    """Main program loop"""
    print("""Peerwise Question Extractor by Joseph. T. Foley<foley AT ru DOT is>
    From https://github.com/foleyj2/teaching-tools""")
    parser = argparse.ArgumentParser(
        description="Load CSV file and manipulate.")
    parser.add_argument('filepaths', nargs=argparse.REMAINDER)# TODO:  one file
    parser.add_argument('--log', default="INFO",
        help='Console log level:  Number or DEBUG, INFO, WARNING, ERROR')

    args = parser.parse_args()
    ## Set up logging
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    print(f"Log level:  {numeric_level}")
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    # log everything to file
    ## TODO:  common logger for all modules
    logpath = 'peerwise-extract-{:%Y%m%d-%H%M%S}.log'.format(datetime.now())
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

    logger.info("Creating Peerwise Extract log file %s", logpath)
    for filepath in args.filepaths:
        # filename pre-processing for output
        inpath = pathlib.PurePath(filepath)
        outpath = inpath.with_suffix(".csq")
        print(f"File: {inpath} -> {outpath}")
        PE = PeerwiseCSV(args.filepaths[0], logger, outpath)
        #PE.dump_values(outfd)
          #print(ER.get_codes()
# STUB:  We know that codes are in column A
# STUB:  We know that we need to update values in column C

if __name__ == "__main__":
  main()
