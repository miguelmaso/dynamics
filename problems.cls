\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{problems}

\LoadClass[12pt]{article}

\RequirePackage[english]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[shortlabels]{enumitem}
\RequirePackage{amsmath}
\RequirePackage{tikz}
\RequirePackage{xcolor}
\RequirePackage{parskip}
\RequirePackage{hyphenat}
\RequirePackage{titlesec}
\RequirePackage{hyperref}


% Definition of some colors
\definecolor{titlebackground}{cmyk}{.16, .0, .42, .0} % pale light lime green
\definecolor{titlebackground}{cmyk}{.24, .03, .07, .02} % duva (blue)
\definecolor{titlebackground}{cmyk}{.09, .55, 1, .39} % moderate gamboe (brown)
\definecolor{titlecolor}{gray}{.95}


% Definition of the sutom title format
\makeatletter
\renewcommand{\maketitle}{
    \noindent
    \colorbox{titlebackground}{\parbox[t][][c]{\textwidth}{
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
    \medskip\par
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


