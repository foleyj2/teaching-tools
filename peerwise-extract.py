#!/usr/bin/env python3
## Process the txt output from Peerwise into a format we can print out
## By Joseph T. Foley <foley AT RU.IS>
## Created 2025-10-13
## Redhat:
##   dnf install texlive-exam texlive-eepic texlive-stix2-otf texlive-lxml-html-clean texlive-gitinfo2
import os
import sys
from pathlib import PurePath##https://docs.python.org/3/library/pathlib.html#module-pathlib
import argparse
import logging
from datetime import datetime
from decimal import *
import random
import sqlite3
## XML
## https://www.geeksforgeeks.org/python/xml-parsing-python/
import xml.etree.ElementTree as ET
#from bs4 import BeautifulSoup
import lxml.html
import lxml.html.clean
## LaTeX abstractions and escaping
from pylatex import Command, Document
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape

class Solution(Environment):
    """Class to wrap LaTeX's solution environment"""
    #packages = [Package("exam")]

class PeerwiseParse():
    DBpath="peerwisexml.db"    
    def __init__(self, infd, logger):
        self.logger = logger       
        # delete our old DB first if it exists
        if os.path.exists(self.DBpath):
            os.remove(self.DBpath)
        self.con = sqlite3.connect(self.DBpath)
        self.con.execute("CREATE TABLE peerwise(tag, question, answer, explanation)")
        self.infd = infd
        self.tags = []
    def load_db(self):
        """Load peerwise XML after adding headers"""
        xmllines = '<?xml version="1.0"?><data>'+"\n"
        for line in self.infd:
            xmllines+=line
        xmllines += "</data>\n"
        def cleantext(xmlstr):
            "XML has lots of encoded characters, clean it up"
            #return BeautifulSoup(xmlstr, "lxml").text
            doc = lxml.html.fromstring(xmlstr)
            cleaner = lxml.html.clean.Cleaner(style=True)
            doc = cleaner.clean_html(doc)
            output = doc.text_content()
            # we still need to remove the Non-breaking spaces \xa0            
            output = ' '.join(output.split())
            # we also need to remove <p> and </p>
            output = output.replace("<p>","")
            output = output.replace("</p>","")           
            return output
        #self.logger.debug(xmlrecords)
        root = ET.fromstring(xmllines)
        self.logger.info(f"# Questions in file: {len(root)}")
        for child in root:
            tag = ""
            question = ""
            explanation = ""
            answer = ""
            alts = {}
            for qdata in child:
                if qdata.tag == "TAGS":
                    tag = cleantext(qdata.text)
                    self.tags.append(tag)
                elif qdata.tag == "QUESTION":
                    question = cleantext(qdata.text)
                elif qdata.tag == "EXPLANATION":
                    explanation = cleantext(qdata.text)
                elif qdata.tag.startswith("ALT"):
                    alts[qdata.tag] = cleantext(qdata.text)
                elif qdata.tag == "ANSWER":
                    answer = alts[f"ALT{qdata.text}"]
            self.logger.debug(f"T:{tag}\nQ:{question}\nA:{answer}")            
            self.con.execute(f"""
                INSERT INTO peerwise VALUES
                {tag, question, answer, explanation}
                """)
        # uniquify the tags
        self.tags = list(set(self.tags))
    def dump_db(self, tag=None):
        dbdump = self.con.execute("SELECT * from peerwise")
        if tag:
            dbdump = self.con.execute(f"SELECT * from peerwise WHERE tag='{tag}'")
        for record in dbdump:
            self.logger.info(record)

    def pick_questions(self, tag, quantity):
        """Subselect [quantity] questions from our pool on a [tag]
        returns:  array of tuples (tag,question,answer,explanation) """
        tagquestions = self.con.execute(f"SELECT * from peerwise WHERE tag='{tag}'")
        questions = []
        for q in tagquestions:
            questions.append(q)
        my_questions = random.sample(questions, quantity)
        return(my_questions)

    def generate_tex(self, filename, question_array, compile=True):
        """Process array into a TeX file then PDF"""        
        doc = Document(filename,documentclass="exam",
                       document_options="a4paper,11pt",
                       textcomp=False)
        tag = question_array[0][0]
        doc.preamble.append(Command("usepackage","multicol"))
        doc.preamble.append(Command("usepackage","stix2"))
        doc.preamble.append(Command("usepackage","siunitx"))
        doc.preamble.append(NoEscape(r'\usepackage[mark]{gitinfo2}'))# I can't figure out how to give package options
        doc.preamble.append(Command("lhead", NoEscape(r"\bfseries\large{} T-865-MADE Oral Exam "
                                                     + tag)))
        doc.preamble.append(Command("rhead","Instructor: Joseph T. Foley"))
        doc.preamble.append(Command("rfoot", NoEscape(r"Page \thepage\ of \numpages")))
        doc.preamble.append(Command("printanswers"))
        doc.append(Command("begin{multicols}{2}"))
        doc.append(Command("begin{questions}"))

        for (tag, question, answer, explanation) in question_array:
            self.logger.debug(f"T{tag},Q:{question},A:{answer}")
            doc.append(Command("question{}"))
            doc.append(question)
            with doc.create(Solution()):
                doc.append(answer)

        doc.append(NoEscape(r"""
        \end{questions}
        \end{multicols}"""))

        doc.generate_pdf(clean_tex=False)
        self.doc = doc
            
def main():
    """Main program loop"""
    print("peerwisexml2tex by Joseph. T. Foley<foley AT ru DOT is>")
    parser = argparse.ArgumentParser(
        description="Process Peerwise txt files into .tex.")
    parser.add_argument('filename',
                        help="Peerwise XML file with data")
    ## TODO:  Fix verbosity based upon another argument and logging
    parser.add_argument('--log', default="INFO",
        help='Console log level:  Number or DEBUG, INFO, WARNING, ERROR')
    parser.add_argument('--tag', default="IA1",
        help='Peerwise tag/topic, e.g. IA1')
    parser.add_argument('--alltags', action='store_true',
        help='Process all tags in the file')
    parser.add_argument('--dumpdb', action='store_true',
        help='Dump the DB and exit')
    parser.add_argument('--quantity', default=20, type=int,
        help='How many questions from the tag')

    args = parser.parse_args()
    ## Set up logging
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    #print(f"Log level:  {numeric_level}")
    logger = logging.getLogger("app")
    logger.setLevel(numeric_level)
    # log everything to file
    logpath = os.path.splitext(args.filename)[0]+".log"
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

    logger.info("Creating Peerwise2TeX log file %s", logpath)

    # filename pre-processing for output
    inpath = PurePath(args.filename)
    print(f"Input: {inpath}")
    input = open(inpath, "r")
    PP = PeerwiseParse(input,logger)
    PP.load_db()
    if args.dumpdb:
        PP.dump_db(tag=args.tag)
        sys.exit()
    tags = [args.tag]
    if args.alltags:
        tags = PP.tags

    for tag in tags:
        print(f"Selecting {args.quantity} questions from topic {tag}")
        questions = PP.pick_questions(args.tag,args.quantity)
        #logger.debug(questions)
        outstem = inpath.stem+"-"+tag
        logger.info("Output: %s.pdf" % outstem)
        PP.generate_tex(outstem, questions)

if __name__ == "__main__":
  main()
