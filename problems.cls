\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{problems}

\LoadClass[12pt]{article}

\RequirePackage[english]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[shortlabels]{enumitem}
\RequirePackage{amsmath}
\RequirePackage{mathtools}
\RequirePackage{tikz}
\RequirePackage{xcolor}
\RequirePackage{parskip}
\RequirePackage{hyphenat}
\RequirePackage{titlesec}
\RequirePackage{hyperref}
\RequirePackage{csquotes}
\RequirePackage[backend=bibtex,style=authoryear]{biblatex}


% Definition of some colors
\definecolor{titlebackground}{cmyk}{.16, .0, .42, .0} % pale light lime green
\definecolor{titlebackground}{cmyk}{.24, .03, .07, .02} % duva (blue)
\definecolor{titlebackground}{cmyk}{.09, .55, 1, .39} % moderate gamboe (brown)
\definecolor{entitybackground}{cmyk}{.04, .27, .5, .25} %
\definecolor{titlecolor}{gray}{.95}


% Definition of the entity field
\makeatletter
\newcommand{\entity}[1]{\gdef\@entity{#1}}%
\newcommand{\@entity}{\@latex@warning@no@line{No \noexpand\entity given}}
\makeatother


% Definition of the custom title format
\makeatletter
\renewcommand{\maketitle}{
    \noindent
    \colorbox{titlebackground}{\parbox[t][][c]{.984\textwidth}{
        \color{titlecolor}{
            \medskip\par\noindent
            \raggedright{\Huge\sffamily\bfseries\@title}
            \bigskip\bigskip\bigskip\par\noindent
            {\large\sffamily\bfseries\@author}
            \hfill
            {\large\sffamily\@date}
            \smallskip
        }
    }}
    {\setlength{\parskip}{-1pt}\par\noindent
    \colorbox{entitybackground}{\parbox{.984\textwidth}{
        \color{titlecolor}{
            \smallskip\par\noindent
            {\sffamily\@entity}
        }
    }}
    }
    \bigskip\par
}
\makeatother


% Removing numbering of sections
\makeatletter
\renewcommand{\@seccntformat}[1]{}
\makeatother


% Definition of the sectioning for examples and solutions
\titleclass{\example}{straight}[\subsection]
\newcounter{example}
\setcounter{secnumdepth}{2}
\titleformat{\example}[runin]{\rmfamily\normalsize\bfseries}{}{0em}{Example~}
\titlespacing*{\example}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}
\newcommand{\exampleautorefname}{example}
\makeatletter
  \def\toclevel@example{2}
\makeatother


% Custom command to align parts of equations
\makeatletter
\newcommand{\pushright}[1]{\ifmeasuring@#1\else\omit\hfill$\displaystyle#1$\fi\ignorespaces}
\newcommand{\pushleft}[1]{\ifmeasuring@#1\else\omit$\displaystyle#1$\hfill\fi\ignorespaces}
\makeatother


% Add link to url in citations
\DeclareFieldFormat{bibhyperref}{\usebibmacro{citelink}{#1}}
\newbibmacro*{citelink}[1]{%
    \iffieldundef{url}
       {\bibhyperref{#1}}
       {\href{\thefield{url}}{#1}}
}
