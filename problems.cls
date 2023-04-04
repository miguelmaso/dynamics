\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{problems}

\LoadClass[12pt]{article}

\RequirePackage[english]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[OT1]{fontenc}
\RequirePackage{mathtools}
\RequirePackage{amsmath}
\RequirePackage{tikz}
\RequirePackage{xcolor}
\RequirePackage{parskip}
\RequirePackage{hyphenat}
\RequirePackage{csquotes}
\RequirePackage[explicit]{titlesec}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[shortlabels]{enumitem}
\RequirePackage[answerdelayed]{exercise}
\RequirePackage[backend=bibtex,style=authortitle]{biblatex}


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


% Removing numbering of sections and setting custom format
\titleformat{\section}{\sffamily\Large\bfseries}{}{0em}{#1}
\titleformat{\subsection}{\sffamily\large\bfseries}{}{0em}{#1}


% Definition of the section level of examples and solutions
\ListOfExerciseInToc
\ExerciseLevelInToc{subsection}


% Definition of the examples and solutions style
\renewcommand{\ExerciseHeader}{\sffamily\normalsize\bfseries
\colorbox{titlebackground}{\color{titlecolor}{
\ExerciseName\ \ExerciseHeaderNB\ }}
\medskip}
 
\renewcommand{\AnswerHeader}{\sffamily\normalsize\bfseries
\colorbox{titlebackground}{\color{titlecolor}{
\hyperref[\ExerciseLabel]{\AnswerName\ \ExerciseHeaderNB\ }}}
\medskip}

\newcommand{\shortAnswer}{
\hyperref[\ExerciseLabel-Answer]{\AnswerListName}:
}


% Definition of the sectioning of examples and solutions
\titleclass{\example}{straight}[\subsection]
\newcounter{example}
\setcounter{secnumdepth}{2}
\titleformat{\example}[runin]{\sffamily\normalsize\bfseries}{}{0em}
    {\hyperref[sol:#1]{\colorbox{titlebackground}{\color{titlecolor}{Example~#1}}}}
    [\label{ex:#1}]
\titlespacing*{\example}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}
\newcommand{\exampleautorefname}{example}
\makeatletter
  \def\toclevel@example{2}
\makeatother


%Solution counterpart
\titleclass{\solution}{straight}[\subsection]
\newcounter{solution}
\setcounter{secnumdepth}{3}
\titleformat{\solution}[runin]{\sffamily\normalsize\bfseries}{}{0em}
    {\hyperref[ex:#1]{\colorbox{titlebackground}{\color{titlecolor}{Solution~#1}}}}
    [\label{sol:#1}]
\titlespacing*{\solution}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}
\newcommand{\solutionautorefname}{solution}
\makeatletter
  \def\toclevel@solution{3}
\makeatother


% Add link to url in citations
\DeclareFieldFormat{bibhyperref}{\usebibmacro{citelink}{#1}}
\newbibmacro*{citelink}[1]{%
    \iffieldundef{url}
       {\bibhyperref{#1}}
       {\href{\thefield{url}}{#1}}
}
