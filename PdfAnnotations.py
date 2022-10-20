#!/usr/bin/python3
## Python manipulation of PDF annotation text
## By Joseph T. Foley <foley AT RU.IS>
## Based upon Enno Groper's answer on Jan 25, 2021 at https://stackoverflow.com/questions/1106098/parse-annotations-from-a-pdf
## This code is modified to work with the newer python3 poppler API
## Ubuntu install 
##  apt install python3-poppler-qt5
## Helpful documentation on Poppler QT5
##    Document https://poppler.freedesktop.org/api/qt5/classPoppler_1_1Document.html
##    Page https://poppler.freedesktop.org/api/qt5/classPoppler_1_1Page.html
##    Annotation https://poppler.freedesktop.org/api/qt5/classPoppler_1_1Annotation.html
from popplerqt5 import Poppler
import sys
#import urllib ##might be useful for extracting from web documents
import os
from pathlib import PurePath##https://docs.python.org/3/library/pathlib.html#module-pathlib
import argparse
import logging
from datetime import datetime


class PdfAnnotations():  
  SubTypes = ("BASE", #0 base class
              "Text", #1 Text callout (bubble)
              "Line", #2 strike out
              "Geometry", #3 geometric figure, like a rectangle or an ellipse. 
              "Highlight",#4 some areas of text being "highlighted"
              "Stamp", #5 drawing a stamp on a page
              "Ink", #6 ink path on a page
              "Link", #7 link to something else (internal or external)
              "Caret", #8 a symbol to indicate the presence of text. 
              "FileAttachment", #9 file embedded in the document
              "Sound", #10 sound to be played when activated.
              "Movie", #11 movie to be played when activated.
              "Screen", #12 screen to be played when activated.
              "Widget", #13 widget (form field) on a page
              "RichMedia" #14 video or sound on a page.
              )
  
  def __init__(self, pdfpath):
    # load from file
    self.annotations = []
    self.document = Poppler.Document.load(pdfpath)
    n_pages = self.document.numPages()
    for i in range(n_pages):
      page = self.document.page(i)
      print(f"Processing page {i+1}")
      for annotation in page.annotations():
        subtype_num = annotation.subType()
        subtype = self.SubTypes[subtype_num]
        #print(f"{subtype_num}={subtype}: {annotation.contents()}")
        anno_record = { "page": page, "subtype": subtype, "contents": annotation.contents() }
        self.annotations.append(anno_record)


  def extract_comments(self, subtypes={"Text","Highlight"}):
    """Dump out all of the comments in a list
    For grading purposes, I only care about the Highlight and Text
    annoation subtypes so they are default"""
    commentlist = []
    for annotation in self.annotations:
      if annotation['subtype'] in subtypes:
        commentlist.append(annotation['contents'])
    return(commentlist)

def main():
    """Main program loop"""
    print("""PDF Annotation Processor by Joseph. T. Foley<foley AT ru DOT is>
    From https://github.com/foleyj2/teaching-tools""")
    parser = argparse.ArgumentParser(
        description="Extract comments from PDF.")
    #    parser.add_argument('--maxval', type=Decimal,
    #                        help='Max value for each grading element.')
    parser.add_argument('filepaths', nargs=argparse.REMAINDER)
    parser.add_argument('--log', default="INFO",
        help='Log level:  Number or DEBUG, INFO, WARNING, ERROR')
    parser.add_argument('--ext', default=".cmt",
                        help='Extension for output')
    args = parser.parse_args()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    datestring = 'PdfAnnotations-{:%Y%m%d-%H%M%S}.log'.format(datetime.now())
    logging.basicConfig(format='%(message)s',
                        filename=datestring, level=numeric_level)
    logging.info("Creating PdfAnnotations log file %s", datestring)

    for filepath in args.filepaths:
      # filename pre-processing for output
      inpath = PurePath(filepath)
      outpath = inpath.with_suffix(args.ext)
      print(f"File: {inpath} -> {outpath}")
      PA = PdfAnnotations(filepath)
      COMMENTS = PA.extract_comments()
      with open(outpath, "w") as outfd:
        for comment in COMMENTS:
          print(comment)

                                  
if __name__ == "__main__":
  main()
