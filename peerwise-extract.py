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

# Installation
## Debian/ubuntu
# sudo apt install python3-bs4

import os
import pathlib
import argparse
import logging
from datetime import datetime
from bs4 import BeautifulSoup
#from collections import OrderedDict
import re
import csv

class PeerwiseCSV():
    """Handle all Peerwise CSV operations."""
    TagDB = {}
    def __init__(self, questionspath, tagspath, logger, outpath):
        self.logger = logger
        # first we load the tags into a DB
        self.logger.info(f"Creating Tag DB from {tagspath}")
        with open(tagspath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.TagDB[int(row["question_id"])]=row["tag"]
        def html2text(htmltext):
            return str(BeautifulSoup(htmltext, 'html.parser').get_text())
                
        # now read the questions
        with open(questionspath, newline="") as csvfile:            
            reader = csv.DictReader(csvfile)
            with open(outpath, "w", newline='') as outputfile:
                writer = csv.writer(outputfile)
                headings = ["timestamp", "tag", "question", "answer"]
                writer.writerow(headings)
                valdimartag_re = re.compile(r"@(IA\d)\s*")
                for row in reader:
                    questionid = int(row["id"])
                    self.logger.debug(f"Processing question ID: {questionid}")
                    questiontext = row["question"]
                    answerchoice = row["answer"]
                    answertext = row["option"+answerchoice]                    
                    # peerwise text is html, so we need to clean it up
                    questiontext = html2text(questiontext)
                    answertext = html2text(answertext)
                    
                    tag = self.TagDB.get(questionid, "")
                    # Valdimar didn't tag his questions right, he used @ID1 at the beginning
                    # TODO:  search the question for @IDX to get the tag
                    if tag == "":
                        self.logger.warning(f"WARNING!  No tags for question {questiontext}")
                        match = valdimartag_re.search(questiontext)
                        if match:
                            tag = match.group(1)
                            self.logger.warning(f"...found in-text tag {tag}, stripping tag from question")
                            questiontext = valdimartag_re.sub("", questiontext)
                    cols = [row["timestamp"], tag, questiontext, answertext]
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
    parser.add_argument('questionspath')# TODO:  one file
    parser.add_argument('tagspath')# TODO:  one file
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
    # filename pre-processing for output
    qpath = pathlib.PurePath(args.questionspath)
    outpath = qpath.with_suffix(".csq")
    print(f"File: {qpath} -> {outpath}")
    PE = PeerwiseCSV(qpath, args.tagspath, logger, outpath)
    #PE.dump_values(outfd)
    #print(ER.get_codes()

if __name__ == "__main__":
  main()
