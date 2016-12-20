\NeedsTeXFormat{LaTeX2e}[1994/06/01]
\ProvidesClass{comsys-letter}[2014/01/03 COMSYS letter adjustments]
\RequirePackage[hidelinks]{hyperref}

\RequirePackage{ifthen}[2001/05/26]
\RequirePackage{datetime2}
%\RequirePackage{letltxmacro}

\newif\ifaccount\accounttrue
\DeclareOption{noaccount}{\accountfalse}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{style/rwth-letter}}

\ProcessOptions\relax



\LoadClass{style/rwth-letter}


\setlength{\parskip}{2ex plus0.5ex minus0.5ex}

\ifaccount
\else
\def\footer{}
\AtBeginDocument{
	\ifschmal\enlargethispage{0mm}\else\enlargethispage{28mm}\fi
}

\fi

\setSender
	{COMSYS}
	{Ahornstra\ss{}e}{55}{E3}
	{52074}{Aachen}
	{Germany}
	{121710}
\setDeanName[Univ.-Prof.\ Dr.-Ing.\ ]{Klaus}{Wehrle}
\def\getSenderName{Klaus~Wehrle}
\ifgerman
	\setDeanFunction{Institutsleiter}
\else
	\setDeanFunction{Head of Institute}
\fi
\setLogo{style/bg/rwth_comsys_rgb.pdf}
\setEMail{wehrle}
\setPhoneTail{21400}
\setFaxTail{22222}
\setPhoneTwoTail{21401}
\setMobil{+49 163 KWEHRLE}
\setFloorNo{0}
\setRoomNo{9011}

\setSignature{KW-\DTMtwodigits{\the\year}\DTMtwodigits{\the\month}\DTMtwodigits{\the\day}}


\def\mfgsigned{\raggedright\noindent\newline\getmfgText%
\hfill\newline\hfill\newline\getSenderName\mfgedtrue%
\\\vspace{-9mm}\includegraphics[height=15mm]{graphics/signature.png}%
%\vspace{7mm}
%\vspace{-\parskip}
}%

%\ifthenelse{\equal{\getpagerefnumber{LastPage}}{1}}{\empty}


%\makeatletter
\setcounter{secnumdepth}{3}
\newcounter {section}
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\newcommand\section{\@startsection {section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\Large\bfseries}}
\newcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\large\bfseries}}
\newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}
\newcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {3.25ex \@plus1ex \@minus.2ex}%
                                    {-1em}%
                                    {\normalfont\normalsize\bfseries}}
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                                       {3.25ex \@plus1ex \@minus .2ex}%
                                       {-1em}%
                                      {\normalfont\normalsize\bfseries}}


\renewcommand\thesection {\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}

\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}



%\makeatother



\endinput
