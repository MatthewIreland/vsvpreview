#!/bin/bash

# Matthew Ireland, 15 July 2015

dir=$1      # absolute path needed
output=$2

cd $dir
for f in *.tex; do
    pdflatex -interaction=nonstopmode -halt-on-error -shell-escape $f &>/dev/null
done

pdftk *.pdf cat output $output
mv $output ..
cd ..
rm -r $dir
