#!/bin/sh
ARGS="--shell-escape --file-line-error --synctex=1 --interaction=nonstopmode"
pdflatex $ARGS problems
biber          problems
pdflatex $ARGS problems
pdflatex $ARGS problems
