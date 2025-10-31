# Dynamics
A collection of examples for the structural dynamics course. The contents of this repo are classified into several parts:
- A static [LaTeX document](https://github.com/miguelmaso/dynamics/blob/gh-pages/problems.pdf) with academic examples
- An interactive extension of the examples with [Jupyter notebooks](ipython/README.md)
- A Python package for processing data recorded at the laboratory.

## LaTeX build
The document is to be compiled using pdflatex and biber, other compilers have not been tested. Run the following [commands](.github/workflows/build_pdf.sh) to compile the document:
```sh
pdflatex problems
biber    problems
pdflatex problems
pdflatex problems
```

### VS Code configuration
If you are using VS Code with a LaTeX extension, make sure the following options are available on the configuration (`ctrl`+`,`):
```jsonc
"latex-workshop.latex.tools": [
  {
    "name": "pdflatex",
    "command": "pdflatex",
    "args": [
      "-synctex=1",
      "-interaction=nonstopmode",
      "-file-line-error",
      "-shell-escape",
      "%DOC%"
    ],
    "env": {}
  },
  {
    "name": "biber",
    "command": "biber",
    "args": [
      "%DOCFILE%"
    ],
    "env": {}
  },
  // other compilation tools
]
```

and

```jsonc
"latex-workshop.latex.recipes": [
  {
    "name": "pdflatex -> biber -> pdflatex * 2",
    "tools": [
      "pdflatex",
      "biber",
      "pdflatex",
      "pdflatex"
    ]
  },
  // other user recipes
]
```
