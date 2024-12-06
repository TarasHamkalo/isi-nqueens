\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tukethesis}[2024/06/23 TUKE Thesis Class, v2024.2]

\PassOptionsToClass{a4paper,12pt,oneside}{report}
\LoadClass{report}

\RequirePackage{nameref}      %% named references
\RequirePackage{pdfpages}

\RequirePackage{titlesec}
\titleformat{\chapter}
    {\huge}{\textbf\thechapter}{20pt}{\huge\textbf}[{\titlerule[0.8pt]}]

\RequirePackage[
    a4paper,
    %width=150mm,
    top=25mm,
    bottom=25mm,
    left=30mm,
    right=25mm,
    bindingoffset=6mm
]{geometry}

\RequirePackage{graphicx}
\DeclareGraphicsExtensions{.pdf,.png,.jpg,.eps}

\definecolor{GitHubBlue}{HTML}{005CC5}
\definecolor{GitHubDarkBlue}{HTML}{032F62}
\definecolor{GitHubGray}{HTML}{6A737D}
\definecolor{GitHubGreen}{HTML}{22863A}
\definecolor{GitHubOrange}{HTML}{E36209}
\definecolor{GitHubPurple}{HTML}{6F42C1}
\definecolor{GitHubRed}{HTML}{D73A49}

\colorlet{Keyword}{GitHubRed}
\colorlet{Function}{GitHubBlue}
\colorlet{Method}{GitHubPurple}
\colorlet{String}{GitHubDarkBlue}
\colorlet{Comment}{GitHubGray}

\RequirePackage{listings}
\lstdefinestyle{default}{
   basicstyle=\small\ttfamily
   showstringspaces=false,
   captionpos=t,
}
\lstset{style=default}

\RequirePackage[
    figure,
    table,
    lstlisting
]{totalcount}

\usepackage{booktabs}
\usepackage{dcolumn}


\RequirePackage{polyglossia}
%% Numeric citations and sorting by citation order
\RequirePackage{csquotes}
\RequirePackage[
    bibencoding=auto,
    style=iso-numeric,      % numeric citations according for ISO 690
    autolang=other,
    sorting=none,           % sort by order of citation
    backend=biber           % different backend
]{biblatex}

\DefineBibliographyStrings{slovak}{%
    bibliography = {Zoznam použitej literatúry}
}

\RequirePackage[
   unicode,
   %backref,
   pdfusetitle,
   %pdfusekeywords,
   pdftoolbar=true,
   pdfmenubar=true,
   pdfwindowui=true,
   bookmarksopenlevel={0},
   bookmarksnumbered,
   bookmarksopen,
   pdfhighlight={/P},
   colorlinks=true,
   %hidelinks, % disable color links completly
   citecolor=magenta,
   linkcolor=magenta,
   filecolor=magenta,
   urlcolor=magenta,
   baseurl={https://kpi.fei.tuke.sk/}
]{hyperref}


\RequirePackage[small]{caption}
\setlength{\captionmargin}{25pt}

\RequirePackage{fancyhdr}
\setlength{\headheight}{15pt}

\pagestyle{fancy}
\renewcommand{\chaptermark}[1]{
    \markboth{\ifnum\value{chapter}>0 \chaptername\ \thechapter.\ \fi #1}{}
}
\fancyhf{}
\rhead{\itshape \nouppercase{\leftmark}}
\rfoot{\thepage}

\fancypagestyle{chapterpage}{
    \fancyhf{}
    \renewcommand\headrulewidth{0pt}
    \rfoot{\thepage}
}

\renewcommand\chapter{
    \if@openright\cleardoublepage\else\clearpage\fi
    \thispagestyle{chapterpage}
    \global\@topnum\z@
    \@afterindentfalse
    \secdef\@chapter\@schapter
}

\renewcommand{\headrulewidth}{0.7pt}


\RequirePackage[
    toc,
    acronym,
    nonumberlist,
    noredefwarn
]{glossaries}
\loadglsentries{glossary}
\makeglossaries % prikaz na vytvorenie suboru .glo


\setcounter{biburllcpenalty}{7000}
\setcounter{biburlucpenalty}{8000}


\counterwithout{footnote}{chapter}


\newcommand{\@thesisspec}{
    \thispagestyle{empty}
    \vspace*{\fill}
    \begin{center}
    \iflanguage{slovak}{
        Tu vložte zadávací list pomocou príkazu\\
        {\texttt{\textbackslash{}thesisspec\{cesta/k/suboru/so/zadavacim.listom\}}}\\
        v preambule dokumentu.

        Kópiu zadávacieho listu skenujte čiernobielo (v odtieňoch sivej) na $200$ až $300$ DPI!
        Nezabudnite do jednej práce vložiť originál zadávacieho listu!
    }{
        Here insert the assignment statement using the command\\
        {\tt{\textbackslash{}thesisspec\{path/to/the/filw/with/assignment.statement\}}}\\
        in the preamble of the document.

        Copy of the assignment statement should be scanned black\&white (grayscale) using DPI from $200$ to $300$!
        Don't forget to insert the original assignment statement into one of the theses copies.
    }
    \end{center}
    \vspace*{\fill}
    \newpage
}
\newcommand{\thesisspec}[1]{
    \renewcommand{\@thesisspec}{
        \includepdf[pages={-}]{#1}
    }
}


\newcommand{\@author@prefix}{}
\newcommand{\@author@firstname}{}
\newcommand{\@author@lastname}{}
\newcommand{\@author@postfix}{}
\renewcommand\author[3][]{
    \renewcommand{\@author@prefix}{#1}
    \renewcommand{\@author@firstname}{#2}
    \renewcommand{\@author@lastname}{#3}
    \authorpostfix
}
\newcommand\authorpostfix[1][]{
    \renewcommand{\@author@postfix}{#1}
}


% DOCVAR: college (The name of the thesis writer's college)
\newcommand{\@college@en}{Technical University of Košice}
\newcommand{\@college@sk}{Technická univerzita v Košiciach}
\newcommand{\@college}{\@college@en}
\newcommand{\college}[2]{
    \renewcommand{\@college@en}{#1}
    \renewcommand{\@college@sk}{#2}
}

\newcommand{\@college@city}{Košice}

% DOCVAR: faculty (The name of the thesis writer's faculty)
\newcommand{\@faculty@en}{Faculty of Electrical Engineering and Informatics}
\newcommand{\@faculty@sk}{Fakulta elektrotechniky a informatiky}
\newcommand{\@faculty}{\@faculty@en}
\newcommand{\faculty}[2]{
    \renewcommand{\@faculty@en}{#1}
    \renewcommand{\@faculty@sk}{#2}
}


% DOCVAR: department (name of the thesis writer's department)
\newcommand{\@department@en}{Department of Computers and Informatics}
\newcommand{\@department@sk}{Katedra počítačov a informatiky}
\newcommand{\@department}{\@department@en}
\newcommand{\department}[2]{
    \renewcommand{\@department@en}{#1}
    \renewcommand{\@department@sk}{#2}
}


% DOCVAR: department's shortcut
\newcommand{\@departmentacr@en}{DCI}
\newcommand{\@departmentacr@sk}{KPI}
\newcommand{\@departmentacr}{\@departmentacr@en}
\newcommand{\departmentacr}[2]{
    \renewcommand{\@departmentacr@en}{#1}
    \renewcommand{\@departmentacr@sk}{#2}
}


% DOCVAR: supervisor (name of the thesis writer's supervisor)
\newcommand{\@supervisor}{}
\newcommand{\supervisor}[1]{\renewcommand{\@supervisor}{#1}}

% DOCVAR: consultant (name of the thesis writer's consultant)
\newcommand{\@consultant}{}
\newcommand{\consultant}[1]{\renewcommand{\@consultant}{#1}}

% DOCVAR: field of study
\newcommand{\@fieldofstudy}{Informatika}
\newcommand{\fieldofstudy}[1]{\renewcommand{\@fieldofstudy}{#1}}

% DOCVAR: study programme
\newcommand{\@studyprogramme}{Informatika}
\newcommand{\studyprogramme}[1]{\renewcommand{\@studyprogramme}{#1}}

% DOCVAR: thesis (type of the thesis)
\newcommand{\@thesis@en}{Bachelor thesis}
\newcommand{\@thesis@sk}{ISI}
\newcommand{\@thesis}{\@thesis@en}
\newcommand{\thesis}[2]{
    \renewcommand{\@thesis@en}{#1}
    \renewcommand{\@thesis@sk}{#2}
}

% DOCVAR: declaration text
\newcommand{\@declaration@en}{I hereby declare that this thesis is my own work and effort. Where other sources of information have been used, they have been acknowledged.}
\newcommand{\@declaration@sk}{Vyhlasujem, že som záverečnú prácu vypracoval(a) samostatne s~použitím uvedenej odbornej literatúry.}
\newcommand{\@declaration}{\@declaration@en}
\newcommand{\declaration}[1]{
    \renewcommand{\@declaration@en}{#1}
    \renewcommand{\@declaration@sk}{#1}
}

% DOCVAR: date (declaration date)
\newcommand{\@submissiondate}{}
\newcommand{\submissiondate}[3]{
    \newcommand{\@submissionday}{#1}
    \newcommand{\@submissionmonth}{#2}
    \newcommand{\@submissionyear}{#3}
}

% DOCVAR: abstract of the thesis
\renewcommand{\abstract}[2]{%
    \newcommand{\@abstract@en}{#1}%
    \newcommand{\@abstract@sk}{#2}%
}
\newcommand{\@abstract}{\@abstract@en}

% DOCVAR: thesis keywords
\newcommand{\keywords}[2]{%
    \newcommand{\@keywords@en}{#1}%
    \newcommand{\@keywords@sk}{#2}%
}
\newcommand{\@keywords}{\@keywords@en}

% DOCVAR: thesis title
\renewcommand{\title}[2]{%
    \newcommand{\@title@en}{#1}%
    \newcommand{\@title@sk}{#2}%
}
\renewcommand{\@title}{\@title@en}


% DOCVAR: thesis (type of the thesis)
\newcommand{\@acknowledgment}{%
    Na tomto mieste by som sa rád poďakoval svojmu vedúcemu záverečnej práce za pripomienky a~odbornú pomoc.
}
\newcommand{\acknowledgment}[1]{\renewcommand{\@acknowledgment}{#1}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Translations of strings used in the thesis
%%
%%%%%

% Default empty declarations
\newcommand{\declarationname}{No Language Selected}
\newcommand{\signaturename}{No Language Selected}
\newcommand{\acknowledgementname}{No Language Selected}
\renewcommand{\lstlistingname}{No Language Selected}
\newcommand{\studyprogrammename}{No Language Selected}
\newcommand{\fieldofstudyname}{No Language Selected}
\newcommand{\departmentname}{No Language Selected}
\newcommand{\supervisorname}{No Language Selected}
\newcommand{\consultantname}{No Language Selected}
\newcommand{\keywordsname}{No Language Selected}
\newcommand{\secondabstractname}{No Language Selected}
\newcommand{\secondkeywordsname}{No Language Selected}
\newcommand{\bibcitationname}{No Language Selected}
\newcommand{\supervisorcitationname}{No Language Selected}
\newcommand{\acrlistname}{No Language Selected}
\newcommand{\appendixlistname}{No Language Selected}


% right page number aligment from 2nd page in table of content
\fancypagestyle{plain}{%
    \renewcommand{\footrulewidth}{0pt}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Front matter
%%
%% - outside and inside front cover
%% - title leaf
%% Do not include the date of make!
%% Institution + department.
%% Names of referees. (optional)
%% Degree.
%% Date of submission and defense. (optional)
%% Place and date of publication and publishers (and other info by them).
%%
%%%%%
\newcommand{\frontmatter}{
    \pagenumbering{roman}
    \pagestyle{empty}  % no page numbers until TOC
    \frontpage
    \titlepage
    \abstractpage

    % thesis detail specification
    \@thesisspec

    \declarationpage
    \acknowledgmentpage

    \pagestyle{plain}
    \tableofcontents
    \newpage

    % show list of figures only if there are some
    \iftotalfigures%
        \listoffigures%
        \newpage%
    \fi

    % show list of tables only if there are some
    \iftotaltables%
        \listoftables%
        \newpage%
    \fi

    % show list of listings only if there are some
    \iftotallstlistings%
        \lstlistoflistings%
        \newpage%
    \fi

    \pagestyle{fancy}
    \pagenumbering{arabic}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Back matter
%%
%%%%%
\newcommand{\backmatter}{
    %% The bibliography
    \printbibliography[heading=bibintoc]

    \label{theend} % the last page of the thesis

    % List of acronyms
    \printglossary[type=\acronymtype,title={\acrlistname}]

    % Glossaries
    \printglossary
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Front page component
%%
%%%%%
\newcommand{\frontpage}{
    \def\br{\\}

    \begin{center}
        {\Large \textbf{\@college}}

        {\Large \textbf{\@faculty}}

        \vfill

        {\LARGE \textbf{\@title} \par}

        \bigskip

        {\large \textbf{\@thesis}}
    \end{center}

    \vfill

    \begin{center}
        {\Large \textbf{\@submissionyear}} \hfill {\Large \textbf{\@author@prefix~\@author@firstname~\@author@lastname~\@author@postfix}}
    \end{center}

    \newpage
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Abstract component
%%
%%%%%

\newcommand{\abstractpage}{
    \def\br{}

    \noindent
    \subsection*{\abstractname}

    \@abstract

    \subsection*{\keywordsname}

    \@keywords

    \iflanguage{slovak}{
        \subsection*{\secondabstractname}

        \begin{otherlanguage}{english}
            \@abstract
        \end{otherlanguage}

        \subsection*{\secondkeywordsname}

        \begin{otherlanguage}{english}
            \@keywords
        \end{otherlanguage}
    }{
        \subsection*{\secondabstractname}

        \begin{otherlanguage}{slovak}
            \@abstract
        \end{otherlanguage}

        \subsection*{\secondkeywordsname}

        \begin{otherlanguage}{slovak}
            \@keywords
        \end{otherlanguage}
    }

    \vfill

    \subsection*{\bibcitationname}

    \MakeUppercase\@author@lastname, \@author@firstname. {\itshape \@title}. \@college@city: \@college, \@faculty, \@submissionyear. \pageref{theend}s. \supervisorcitationname: \@supervisor

    \newpage

    \def\br{\\}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Declaration component
%%
%%%%%
\newcommand\declarationpage{
    \vglue0pt
    \vfill
    \subsection*{\declarationname}

    \noindent\@declaration

%    \bigskip
%
%    \noindent \@college@city,~\@submissionday.\@submissionmonth.\@submissionyear \hfill
%    \begin{tabular}[t]{c}
%        \hbox to 50mm {\dotfill} \\ \textit{\small \signaturename}
%    \end{tabular}
    \newpage
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Declaration component
%%
%%%%%
\newcommand\acknowledgmentpage{%
    \vglue0pt\vfill%

    \subsection*{\acknowledgementname}%

    \@acknowledgment

    \newpage
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Title page component
%%
%%%%%
\renewcommand{\titlepage}{
    \begin{center}
        {\Large \textbf{\@college}}

        {\Large \textbf{\@faculty}}

        \vfill

        {\LARGE \textbf{\@title} \par}

        \bigskip

        {\large \textbf{\@thesis}}
    \end{center}

    \vfill

    \noindent
    \begin{tabular}{@{}p{.26\textwidth}p{.7\textwidth}}
        \studyprogrammename:& \@studyprogramme \\
        \fieldofstudyname:& \@fieldofstudy \\
        \departmentname:& \@department~(\@departmentacr) \\
        \supervisorname:& \@supervisor \\
        \if\@consultant\empty\else\consultantname:& \@consultant \\ \fi
    \end{tabular}

    \vspace{2\baselineskip}

    \begin{center}
        \centering
        {\Large \textbf{\@college@city{} \@submissionyear}} \hfill {\Large \textbf{\@author@prefix~\@author@firstname~\@author@lastname~\@author@postfix}}
    \end{center}

    \newpage
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Font Settings
%%
%%%%%

% Set the fonts
\RequirePackage{fontspec}
\setmainfont{TeX Gyre Pagella}   % \rmfamily{}
\setsansfont{TeX Gyre Heros}[Scale=MatchLowercase]   % \rmfamily{}
\setmonofont[
    Path = ./fonts/,
    UprightFont = *-Regular.otf,
    BoldFont = *-Bold.otf,
    ItalicFont = *-It.otf,
    BoldItalicFont = *-BoldIt.otf,
    Scale=MatchLowercase
]{SourceCodePro}   % \ttfamily{}

% Set math font
\RequirePackage{unicode-math}
\setmathfont{TeX Gyre Pagella Math}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% Line spacing and paragraph indentation
%%
%%%%%

\linespread{1.3}
\setlength{\parindent}{1.5em}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\AtBeginDocument{
    \addto\captionsenglish{
        \renewcommand{\@title}{\@title@en}
        \renewcommand{\@abstract}{\@abstract@en}
        \renewcommand{\@keywords}{\@keywords@en}
        \renewcommand{\@college}{\@college@en}
        \renewcommand{\@department}{\@department@en}
        \renewcommand{\@departmentacr}{\@departmentacr@en}
        \renewcommand{\@faculty}{\@faculty@en}
        \renewcommand{\@thesis}{\@thesis@en}
        \renewcommand{\@declaration}{\@declaration@en}
        \renewcommand{\declarationname}{Declaration}
        \renewcommand{\signaturename}{Signature}
        \renewcommand{\acknowledgementname}{Acknowledgement}
        \renewcommand{\studyprogrammename}{Study Programme}
        \renewcommand{\fieldofstudyname}{Field of Study}
        \renewcommand{\departmentname}{Department}
        \renewcommand{\supervisorname}{Supervisor}
        \renewcommand{\consultantname}{Consultant}
        \renewcommand{\abstractname}{Abstract in English}
        \renewcommand{\keywordsname}{Keywords in English}
        \renewcommand{\secondabstractname}{Abstract in Slovak}
        \renewcommand{\secondkeywordsname}{Keywords in Slovak}
        \renewcommand{\bibcitationname}{Bibliographic Citation}
        \renewcommand{\supervisorcitationname}{Supervisor}
        \renewcommand{\acrlistname}{List of Abbreviations}
        \renewcommand{\appendixlistname}{List of Appendixes}
        \renewcommand{\lstlistingname}{Listing}
        \renewcommand{\lstlistlistingname}{List of \lstlistingname s}
        \renewcommand{\figurename}{Figure}
    }
    \addto\captionsslovak{
        \renewcommand{\@title}{\@title@sk}
        \renewcommand{\@abstract}{\@abstract@sk}
        \renewcommand{\@keywords}{\@keywords@sk}
        \renewcommand{\@college}{\@college@sk}
        \renewcommand{\@department}{\@department@sk}
        \renewcommand{\@departmentacr}{\@departmentacr@sk}
        \renewcommand{\@faculty}{\@faculty@sk}
        \renewcommand{\@thesis}{\@thesis@sk}
        \renewcommand{\@declaration}{\@declaration@sk}
        \renewcommand{\declarationname}{Čestné vyhlásenie}
        \renewcommand{\signaturename}{Vlastnoručný podpis}
        \renewcommand{\acknowledgementname}{Poďakovanie}
        \renewcommand{\studyprogrammename}{Študijný program}
        \renewcommand{\fieldofstudyname}{Študijný odbor}
        \renewcommand{\departmentname}{Školiace pracovisko}
        \renewcommand{\supervisorname}{Školiteľ}
        \renewcommand{\consultantname}{Konzultant}
        \renewcommand{\abstractname}{Abstrakt v SJ}
        \renewcommand{\keywordsname}{Kľúčové slová v SJ}
        \renewcommand{\secondabstractname}{Abstrakt v AJ}
        \renewcommand{\secondkeywordsname}{Kľúčové slová v AJ}
        \renewcommand{\bibcitationname}{Bibliografická citácia}
        \renewcommand{\supervisorcitationname}{Vedúci práce}
        \renewcommand{\acrlistname}{Zoznam skratiek}
        \renewcommand{\appendixlistname}{Zoznam príloh}
        \renewcommand{\appendixname}{Príloha}
        \renewcommand{\appendixautorefname}{Príloha}
        \renewcommand{\lstlistingname}{Výpis}
        \renewcommand{\lstlistlistingname}{Zoznam výpisov}
        \renewcommand{\figurename}{Obrázok}
    }
}

% Polyglossia sets the language only in \AfterEndPreambule
\AfterEndPreamble{
    % PDF metadata based on macro values and current language
    \def\br{}
    \iflanguage{english}{
        \hypersetup{
            pdftitle = {\@title@en},
            pdfauthor = {\@author@firstname~\@author@lastname},
            pdfkeywords = {\@keywords@en},
            pdfsubject = {\@thesis@en}
        }
    }{
        \hypersetup{
            pdftitle = {\@title@sk},
            pdfauthor = {\@author@firstname~\@author@lastname},
            pdfkeywords = {\@keywords@sk},
            pdfsubject = {\@thesis@sk}
        }
    }
}
