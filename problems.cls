\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{problems}

\LoadClass[12pt]{article}

\RequirePackage[english]{babel}
\RequirePackage[utf8]{inputenc}
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
\definecolor{titlecolor}{gray}{.90}


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


% Definition of nse sectioning for problems and solutions
\titleclass{\problem}{straight}[\subsection]
\newcounter{problem}
\setcounter{secnumdepth}{2}
\titleformat{\problem}[runin]{\rmfamily\normalsize\bfseries}{}{0em}{Problem~}
\titlespacing*{\problem}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}
\newcommand{\problemautorefname}{problem}
\makeatletter
  \def\toclevel@problem{2}
\makeatother
