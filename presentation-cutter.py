#!/usr/bin/python3
PROGDESCRIPTION = """Processor for end-of-term presentations which are collections of feedback (multiple per page)
We need to separate them so that they can be handed back to the students
Remember to install pdfcrop first, which is in texlive-extra-utils on debian systems.
By Joseph T. Foley <foley AT ru DOT is>
$Id: presentation-cutter.py 634 2019-11-19 10:36:43Z foley $
$URL: https://repository.cs.ru.is/svn/t-411-mech-instructor/grades/presentation/scans/presentation-cutter.py $
"""

import argparse
import subprocess

class Pdfcropper(object):
    """Take a pdf file and selectively crop to only the right area"""
    ## choose the areas in mm, we will convert into pt for pdfcrop
    ## values should be negative to show that we are removing sections
    ## order:  left, top, right, bottom
    ## TODO:  Fix the grading sheet to have more consistent spacing
    ##        otherwise we have to do tweaks.
    areamm = {'top': [0,-15,0,-192],
             'mid': [0,-110,0,-102],
             'bot': [0,-192,0,0],}
    args = None
    mm2pt = 2.83465 
    
    def __init__(self, args):
        "Setup with the given arguments"
        self.args = args
    def crop(self):
        "Crop the file"
        areamm = self.areamm[self.args.region]
        areapt = [str(i*self.mm2pt) for i in areamm]
        areaarg = " ".join(areapt)
        cmd = ['pdfcrop','--margins',areaarg,args.infile,args.outfile]
        #print(cmd)
        subprocess.run(cmd)

if __name__ == '__main__':  #Main invocation
    parser = argparse.ArgumentParser(description="PROGDESCRIPTION")
    parser.add_argument('infile',
                        help='PDF filepath containing the scans of presentation feedback')
    parser.add_argument('outfile',
                        help='Output filepath')
    parser.add_argument('region', choices=['top','mid','bot'])

    args = parser.parse_args()
    pdfcropper = Pdfcropper(args)
    pdfcropper.crop()
    

