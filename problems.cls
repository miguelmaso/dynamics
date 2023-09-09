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
\RequirePackage{siunitx}
\RequirePackage{hyphenat}
\RequirePackage{csquotes}
\RequirePackage{fancyhdr}
\RequirePackage{xstring}
\RequirePackage{catchfile}
\RequirePackage[explicit]{titlesec}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[shortlabels]{enumitem}
\RequirePackage[answerdelayed]{exercise}
\RequirePackage[backend=bibtex,style=authortitle]{biblatex}


% Definition of the git revision tag
\CatchFileDef{\head}{.git/HEAD}{}
\StrGobbleRight{\head}{1}[\head]
\StrBehind[2]{\head}{/}[\branch]
\IfFileExists{.git/refs/heads/\branch}{
    \CatchFileDef{\hash}{.git/refs/heads/\branch}{}
    \newcommand{\gitrevision}{rev \StrLeft{\hash}{7}}
}{
    \newcommand{\gitrevision}{}
}


% Definition of some colors
\definecolor{titlebackground}{cmyk}{.09, .55, 1, .39}    % moderate gamboe (brown)
\definecolor{entitybackground}{cmyk}{.04, .27, .5, .25}  % light brown
\definecolor{titlecolor}{gray}{.95}


% Definition of the entity field
\makeatletter
\newcommand{\entity}[1]{\gdef\@entity{#1}}%
\newcommand{\@entity}{\@latex@warning@no@line{No \noexpand\entity given}}
\makeatother


% Definition of the short title field
\makeatletter
\renewcommand{\title}[2][]{\gdef\shorttitle{#1}\gdef\@title{#2}}
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
    \colorbox{entitybackground}{\parbox[t][][c]{.984\textwidth}{
        \color{titlecolor}{
            \smallskip\par\noindent
            {\sffamily\@entity}
        }
    }}
    }
    \bigskip\par
    \thispagestyle{empty}
}
\makeatother


% Definition of the custom pagestyle
\fancypagestyle{problems}{
    \setlength{\headheight}{35pt}
    \addtolength{\topmargin}{-20pt}
    \renewcommand{\headrulewidth}{0pt} % remove lines as well
    \renewcommand{\footrulewidth}{0pt}
    \fancyhead[L]{\scshape\shorttitle}
    \fancyhead[R]{\raisebox{-0.2\height}{\includegraphics[height=35pt]{img/camins.jpeg}}}
    \fancyfoot[R]{\footnotesize\color{gray}\gitrevision}
}
\pagestyle{problems}


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
\smallskip}

\renewcommand{\AnswerHeader}{\sffamily\normalsize\bfseries
\colorbox{titlebackground}{\color{titlecolor}{
\hyperref[\ExerciseLabel]{\AnswerName\ \ExerciseHeaderNB\ }}}
\smallskip}

\newcommand{\shortAnswer}{
\hyperref[\ExerciseLabel-Answer]{\AnswerListName}:
}


% Add link to url in citations
\DeclareFieldFormat{bibhyperref}{\usebibmacro{citelink}{#1}}
\newbibmacro*{citelink}[1]{%
    \iffieldundef{url}
       {\bibhyperref{#1}}
       {\href{\thefield{url}}{#1}}
}
