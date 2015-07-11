#!/bin/bash

for f in part*; do
    cp template.tex "${f}.2"
    sed -i "s/%%%SOURCE%%%/${f}/g" "${f}.2"
    pdflatex "${f}.2"
    mv "${f}.2.pdf" ${f}.pdf
done

pdftk *.pdf cat output OUT.pdf
