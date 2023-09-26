#!/bin/sh

pdflatex problems
biber    problems
pdflatex problems
pdflatex problems
