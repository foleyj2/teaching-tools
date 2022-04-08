#!/bin/bash
## Ubuntu:  sudo apt install poppler
sections=(SEC1 SEC2 SEC3)
mkdir -p bound-pdfs
for s in ${sections[@]}; do
    pdfunite *${s}.pdf bound-pdfs/${s}.pdf
done
