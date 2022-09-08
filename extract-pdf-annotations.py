#!/usr/bin/python3
## Python extraction of PDF annotation text for grading purposes
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

def main():
  # TODO:  modularize for use in other tools
  # TODO:  better argument parsing
  input_filename = sys.argv[1]
  document = Poppler.Document.load(input_filename)
  n_pages = document.numPages()
  all_annots = 0

  for i in range(n_pages):
    page = document.page(i)    
    for annotation in page.annotations():
      subtype_num = annotation.subType()
      subtype = SubTypes[subtype_num]
      #print(f"{subtype_num}={subtype}: {annotation.contents()}")

      ## For grading purposes, I only care about the Highlight and Text
      ## annoation subtypes
      if subtype in {"Text","Highlight"}:     
        print(f"Annotation suitable for grading: '{annotation.contents()}'")
                                  
      #print(f"SubType:TextAnnotation: {annotation.SubType()}")
      ## Poppler::Annotation::SubType TextAnnoation
    if len(page.annotations()) < 1:      
      print("no annotations found")

if __name__ == "__main__":
  main()
