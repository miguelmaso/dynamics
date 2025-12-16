#!/bin/sh
ARGS="--shell-escape --file-line-error --synctex=1 --interaction=nonstopmode"
mkdir img/figures/
pdflatex $ARGS problems
biber          problems
pdflatex $ARGS problems
pdflatex $ARGS problems
