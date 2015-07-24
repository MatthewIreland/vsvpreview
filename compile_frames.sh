#!/bin/bash

# Matthew Ireland, 15 July 2015

dir=$1
output=$2
meta_dir=$3

cd $dir

for f in $(ls -1 $meta_dir | grep -v "pdf" | grep -v "tex"); do
    ln -s "$meta_dir/$f" .
done

for f in *.tex; do
    pdflatex -interaction=nonstopmode -halt-on-error -shell-escape $f &>/dev/null
done

pdftk *.pdf cat output $output
mv $output ../..
dir=$(pwd)
cd ..
#rm -r $dir
