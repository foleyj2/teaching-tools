#!/usr/bin/env python3
## Tool to anonymize peer review files
## Author:  Joseph T. Foley <foley AT RU DOT IS>
## Start Date: 2024-11-16
## Input:  path to files
## Output:  new folder anon with files renamed with random sequence numbers
import os
from os.path import isfile, join
import argparse
import logging

"""Main program loop"""
print("""Anonmyzer of Files by Joseph. T. Foley<foley AT ru DOT is>
From https://github.com/foleyj2/teaching-tools""")
parser = argparse.ArgumentParser(
    description="Anonymize directory of files.")
parser.add_argument('filepath')

args = parser.parse_args()

# get list of filenames from the path
origfiles = [f for f in os.listdir(args.filepath)
             if isfile(join(args.filepath, f))]
print(origfiles)
