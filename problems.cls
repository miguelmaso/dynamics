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
\RequirePackage{footnote}
\RequirePackage[symbol*]{footmisc}
\RequirePackage[explicit]{titlesec}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[shortlabels]{enumitem}
\RequirePackage[margin=2.5cm]{geometry}
\RequirePackage[answerdelayed]{exercise}
\RequirePackage[style=authortitle]{biblatex}


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
    \savenotes
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
    \hspace*{-1pt}\spewnotes
    {\setlength{\parskip}{-1pt}\par\noindent
    \colorbox{entitybackground}{\parbox[t][][c]{.984\textwidth}{
        \color{titlecolor}{
            \smallskip\par\noindent
            {\sffamily\@entity}
        }
    }}\\
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

\renewcommand{\AnswerName}{Answer to Exercise}
\renewcommand{\AnswerHeader}{\sffamily\normalsize\bfseries
\colorbox{titlebackground}{\color{titlecolor}{
\hyperref[\ExerciseLabel]{\AnswerName\ \ExerciseHeaderNB\ }}}
\smallskip}

% Short answer label with link if extended answer defined
\makeatletter
\newcommand{\silentref}[2]{
    \@ifundefined{r@#1}{#2}{\hyperref[#1]{#2}}
}
\makeatother
\newcommand{\shortAnswer}{
    \silentref{\ExerciseLabel-Answer}{\AnswerListName}:
}


% Globally set the item enumeration with small cap letter
\renewcommand{\theenumi}{\alph{enumi}}


% Tikz libraries and speedup compilation
\usetikzlibrary{calc}
\usetikzlibrary{external}
\tikzexternalize[prefix=img/]


% Add link to url in citations
\DeclareFieldFormat{bibhyperref}{\usebibmacro{citelink}{#1}}
\newbibmacro*{citelink}[1]{%
    \iffieldundef{url}
       {\bibhyperref{#1}}
       {\href{\thefield{url}}{#1}}
}


% Enforce hyphenation of urls
\def\UrlBreaks{\do\/\do\a\do\b\do\c\do\d\do\e\do\f\do\g\do\h\do\i\do\j\do\k\do\l\do\m\do\n\do\o\do\p\do\q\do\r\do\s\do\t\do\u\do\v\do\w\do\x\do\y\do\z\do\A\do\B\do\C\do\D\do\E\do\F\do\G\do\H\do\I\do\J\do\K\do\L\do\M\do\N\do\O\do\P\do\Q\do\R\do\S\do\T\do\U\do\V\do\W\do\X\do\Y\do\Z\do0\do1\do2\do3\do4\do5\do6\do7\do8\do9\do=\do/\do.\do:}
\setcounter{biburllcpenalty}{9000}
