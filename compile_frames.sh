#!/bin/bash

# Matthew Ireland, 15 July 2015

dir=$1
output=$2
meta_dir=$3

cd $dir

for f in $(ls -1 $meta_dir | grep -v "pdf" | grep -v "tex"); do
    #ln -s "$meta_dir/$f" .
    :
done

for f in *.tex; do
	#dos2unix $f
	echo -n "."
    pdflatex -interaction=nonstopmode -halt-on-error -shell-escape "$f" &>/dev/null
#    if [ -e part0000.tex ]; then
#    	pdflatex -interaction=nonstopmode -halt-on-error -shell-escape "part0000.tex" &>/dev/null
#    fi
done

echo ""

# Remove any pdfs resulting from empty frames.
find . -size  0 -print0 | xargs -0 rm

pdftk *.pdf cat output $output
mv $output ../..
dir=$(pwd)
cd ..
rm -r $dir
