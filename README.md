# Dynamics
A collection of examples for the structural dynamics course. The examples are classified in two parts:
- A static [LaTeX document](https://github.com/miguelmaso/dynamics/blob/gh-pages/problems.pdf)
- An interactive extension of [Jupyter notebooks](ipython/README.md)

## LaTeX build
The document has been comiled using pdflatex and biber, other compilers have not been tested. To compile the document, run the following [commands](.github/workflows/build_pdf.sh):
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
