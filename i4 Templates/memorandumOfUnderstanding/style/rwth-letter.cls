% rwth-letter.cls
%
% Diese Klasse ist im Auftrag der RWTH Aachen entstanden.
% Sie dient der Umsetzung des Corporate Design der RWTH in LaTeX.
% 
% Die Klasse wird mit dem Paket rwth-base(.sty) mitgeliefert.
%
% Autor: Jens Dodenhoff (jens.dodenhoff@rwth-aachen.de)
% 
\NeedsTeXFormat{LaTeX2e}[1994/06/01]
\ProvidesClass{rwth-letter}[2013/11/22 RWTH Briefvorlage]

% file pointers, counters, booleans
\newread\myread
\newcounter{linecnt}
\newcounter{konten}
\setcounter{konten}{0}
\newcounter{attCount}
\setcounter{attCount}{0}
\newif\ifattached\attachedfalse
\newif\iffolded\foldedfalse
\newif\ifunblock\unblocktrue
\newif\ifmfged\mfgedfalse
\newif\ifschmal\schmalfalse
\newif\ifwieskeed\wieskeedfalse
\newif\ifamerican\americanfalse
\newif\ifbritish\britishfalse
\newif\ifgerman\germantrue
\newif\ifngerman\ngermantrue
\newif\ifdutch\dutchfalse
\newif\ifprintdate\printdatetrue


% class and all needed packages
\LoadClass{minimal}%[2001/05/25]
\RequirePackage{afterpage}[1995/10/27]
\RequirePackage{ifthen}[2001/05/26]
\RequirePackage{refcount}[2010/12/01]
\RequirePackage{graphicx}[1999/02/16]
\RequirePackage[absolute]{textpos}[2010/09/30]
% options
\DeclareOption{dutch}{\americanfalse\britishfalse\ngermanfalse\germanfalse\dutchtrue}
\DeclareOption{german}{\americanfalse\britishfalse\ngermanfalse\germantrue\dutchfalse}
\DeclareOption{ngerman}{\americanfalse\britishfalse\germantrue\ngermantrue\dutchfalse}
% the next three are synonymous according to docs
\DeclareOption{american}{\americantrue\britishfalse\germanfalse\ngermanfalse\dutchfalse}
\DeclareOption{english}{\americantrue\britishfalse\germanfalse\ngermanfalse\dutchfalse}
\DeclareOption{USenglish}{\americantrue\britishfalse\germanfalse\ngermanfalse\dutchfalse}
% the next two are synonymous according to docs
\DeclareOption{UKenglish}{\americantrue\britishtrue\germanfalse\ngermanfalse\dutchfalse}
\DeclareOption{british}{\americantrue\britishtrue\germanfalse\ngermanfalse\dutchfalse}
\DeclareOption{nomfg}{\mfgedtrue}
\DeclareOption{list}{\attachedtrue}
\DeclareOption{block}{\unblockfalse}
\DeclareOption{foldmarks}{\foldedtrue}
\DeclareOption{faltmarken}{\foldedtrue}
\DeclareOption{tight}{\schmaltrue}
\DeclareOption{schmal}{\schmaltrue}
\DeclareOption{nodate}{\printdatefalse}
%\DeclareOption{mathtext}{\PassOptionsToPackage{\CurrentOption}{rwth-base}}
% alle anderen optionen einfach an rwth-base weiterleiten
% hiernach koennen keine weiteren optionen deklariert werden
\DeclareOption*{\PassOptionsToPackage{\CurrentOption}{rwth-base}}
\ProcessOptions\relax
\RequirePackage{style/rwth-base}[2013/11/22]

% paper format a4
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\textblockorigin{0mm}{0mm}
\setlength{\unitlength}{1mm}
\setlength{\oddsidemargin}{20mm}
\addtolength{\oddsidemargin}{-1in}
\setlength{\evensidemargin}{\oddsidemargin}
\ifschmal\setlength{\textwidth}{130mm}\else\setlength{\textwidth}{170mm}\fi
%\ifschmal\setlength{\textwidth}{130mm}\else\setlength{\textwidth}{182.5mm}\fi
\setlength{\paperwidth}{210mm}
\setlength{\paperheight}{297mm}
\setlength{\topmargin}{-1in}
\setlength{\hoffset}{0mm}
\setlength{\voffset}{0mm}
\setlength{\headsep}{0mm}
\setlength{\parindent}{0mm}
\setlength{\parskip}{0mm}

\def\ps@rwthpage{%
\setlength{\textheight}{248mm}%
\setlength{\headheight}{96mm}% dies plus topmargin sind 96mm vom oberen seitenrand, obere Rand der Betreffzeile
\setlength{\footskip}{5mm}% dies sollte auf 13mm abstand vom unteren seitenrand bedeuten
\ifschmal%
	% the following leads to 158.5mm distance to left rim
	% and w/o hspace to an overfull hbox
	\def\@oddfoot{\hspace{138.5mm}\pagelabel\hfill\hspace{-20mm}}%
%\else\def\@oddfoot{\hfill\pagelabel}%
\else\def\@oddfoot{\hspace{179mm}\pagelabel\hfill\hspace{-20mm}}%
\fi
\def\@evenfoot{\@oddfoot}}

% sprachsensitive befehle
% abhaengig von sprache:
\ifamerican
	\ifbritish\else
		\RequirePackage[american]{babel}
	\fi
	\def\getUStIdText{VAT Identification Number}%
	\def\getSteuerText{Tax Number}%
	\def\getKontoText{Account}%
	\def\getBLZText{BIN}%
	\def\getBuildText{Building}%
	\def\getRoomText{Room}%
	\def\getFloorText{Floor}%
	\def\getPhoneText{Phone:\hspace{0.5ex}}%
	\def\getMobilText{Cell:\hspace{2.8ex}}%
	\def\getFaxText{Fax:\hspace{3ex}}%
	\def\getSignatureText{Signature:}%
	\def\getInvoiceNumberText{Invoice number:}%
	\def\getAnlagenText{Attachment}%
	\def\getmfgText{Kind regards}%
	\def\getSubjectText{No subject}%
	\def\getSalutation{Dear Sir or Madam:}
\fi
\ifbritish
	\RequirePackage[british]{babel}
	\renewcommand{\getMobilText}{Mobile:\hspace{.5ex}}%
	\renewcommand{\getSalutation}{Dear Sir or Madam}
\fi
\ifgerman
	\ifngerman\else
		\RequirePackage[german]{babel}
	\fi
	\def\getUStIdText{USt-Identifikationsnummer}%
	\def\getSteuerText{Steuernummer}%
	\def\getKontoText{Konto}%
	\def\getBLZText{BLZ}%
	\def\getBuildText{Geb\"{a}ude}%
	\def\getRoomText{Raum~Nr.}%
	\def\getFloorText{Geschoss}%
	\def\getPhoneText{Telefon:}%
	\def\getMobilText{Mobil:\hspace{1.5ex}}%
	\def\getFaxText{Fax:\hspace{3ex}}%
	\def\getSignatureText{Mein Zeichen:}%
	\def\getInvoiceNumberText{Rechnungsnummer:}%
	\def\getAnlagenText{Anlagen}%
	\def\getmfgText{Mit freundlichen Gr\"{u}\ss en}%
	\def\getSubjectText{Kein Betreff}%
	\def\getSalutation{Sehr geehrte Damen und Herren,}
\fi
\ifngerman
	\RequirePackage[ngerman]{babel}
	% falls sich irgendwas in ngerman von german unterscheidet
\fi
\ifdutch
	\RequirePackage[dutch]{babel}
	\def\getUStIdText{Omzetbelastingnummer}%
	\def\getSteuerText{Belastingnummer}%
	\def\getKontoText{Rekening}%
	\def\getBLZText{Banknummer}%
	\def\getBuildText{Gebouw}%
	\def\getRoomText{Kamer~Nr.}%
	\def\getFloorText{Etage}%
	\def\getPhoneText{Telefoon:}%
	\def\getMobilText{Mobiel:\hspace{1.5ex}}%
	\def\getFaxText{Fax:\hspace{4ex}}%
	\def\getSignatureText{Mijn kenmerk:}%
	\def\getInvoiceNumberText{Faktuurnummer:}%
	\def\getAnlagenText{Ingesloten stuk}%
	\def\getmfgText{Met vriendelijke groeten}%
	\def\getSubjectText{Geen onderwerp}%
	\def\getSalutation{Geachtes dames en heren,}
\fi
%unabhaengig von sprache
	\def\getSWIFTText{SWIFT-BIC}%
	\def\getIBANText{IBAN}%
% konstanten
\def\RWTHPAGE{rwth-aachen.de}
\def\getPhonePrefix{+49~241~80}
\def\getBank{Sparkasse~Aachen}
\def\getBIN{390~500~00}
\def\getIBAN{DE34~3905~0000~0000~0145~22}
\def\getSWIFT{AACSDE33XXX}
\def\getUStId{DE~121~689~807}
\def\getSteuerNummer{201/5930/5005}
% echte set-Funktionen
\def\setWWW#1{\def\getWWW{www\ifthenelse{\equal{#1}{\empty}}{}{.\MakeLowercase{#1}}.\RWTHPAGE}}\setWWW\empty
\def\setRemark#1{\def\getRemark{#1}}\setRemark{\hfill}
\def\setLogo#1{\def\getLogo{#1}}\setLogo{rwth_im_rgb}
\def\setRoomNo#1{\def\getRoomNo{#1}}\setRoomNo{\empty}
\def\setFloorNo#1{\def\getFloorNo{#1}}\setFloorNo{\empty}
\def\setDeanFunction#1{\def\getDeanFunction{\ifthenelse{\equal{#1}{\empty}}{}{#1\newline}}}\setDeanFunction{\empty}
\def\setSenderFunction#1#2{}\renewcommand{\setSenderFunction}[2][\empty]{\def\getSenderFunction{#2\newline\ifthenelse{\equal{#1}{\empty}}{}{#1\newline}}}\setSenderFunction{\empty}
\def\setInvoiceNumber#1{\def\getInvoiceNumber{#1}}\setInvoiceNumber{\empty}
\def\setSignature#1{\def\getSignature{#1}}\setSignature{\empty}
\def\setSubject#1{\def\getSubject{\begin{flushleft}\noindent\textbf{#1}\newline\hfill\newline\hfill\end{flushleft}}}\setSubject{\getSubjectText}
\def\setEMail#1#2{}\renewcommand{\setEMail}[2][\getSenderKurz]{\def\getEMail{\MakeLowercase{#2}@\ifschmal\newline\fi\ifthenelse{\equal{#1}{\empty}}{}{\MakeLowercase#1.}\RWTHPAGE}}
%\def\setEMail#1#2{}\renewcommand{\setEMail}[2][\getSenderKurz]{\def\getEMail{\MakeLowercase{#2}@\ifschmal\newline\fi\ifthenelse{\equal{\getSenderKurz}{\empty}}{}{\MakeLowercase\getSenderKurz.}\RWTHPAGE}}
\def\setMobil#1{\def\getMobil{#1}}\setMobil{\empty}
\def\setPhoneTail#1#2{}\renewcommand{\setPhoneTail}[2][\getPhonePrefix]{\def\getPhone{#1-#2}}\setPhoneTail{1}
\def\setPhoneTwoTail#1#2{}\renewcommand{\setPhoneTwoTail}[2][\getPhonePrefix]{\def\getPhoneTwo{#1-#2}}\setPhoneTwoTail{1}
\def\setFaxTail#1#2{}\renewcommand{\setFaxTail}[2][\getPhonePrefix]{\def\getFax{#1-#2}}\setFaxTail{92312}
% set Funktionen mit Annahmen
\def\setSenderName#1#2#3{}\renewcommand{\setSenderName}[3][\empty]{%
		\setEMail{#2.#3}%
		\def\getSenderName{#2~#3}%
		\def\getSenderFullName{\ifthenelse{\equal{#1}{\empty}}{}{#1~}\ifschmal\hfill\newline\fi\ifthenelse{\equal{#2}{\empty}}{}{#2~}#3}%
		}\setSenderName{}{}
\def\setDeanName#1#2#3{}\renewcommand{\setDeanName}[3][\empty]{%
		\def\getDeanName{#2~#3}%
		\def\getDeanFullName{\ifthenelse{\equal{#1}{\empty}}{}{#1~}\ifschmal\hfill\newline\fi\ifthenelse{\equal{#2}{\empty}}{}{#2~}#3}%
		}\setDeanName{}{}
\def\setKonto#1#2#3#4#5#6{\addtocontents{acc}{\protect\kontoblock{#1}{#2}{#3}{#4}{#5}{#6}}}
\def\setAdress#1#2#3#4#5#6#7#8#9{
	\addtocontents{adr}{\protect\layoutAdress{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}{#9}}
	\def\getHonorific{#1}
	\def\getFirm{#2}
	\def\getContact{#3}
	\def\getStreet{#4}
	\def\getHNo{#5}
	\def\getBuildNo{#6}
	\def\getPostcode{#7}
	\def\getCity{#8}
	\def\getCountry{#9}
	}\setAdress{}{}{}{}{}{}{}{}{}
\def\setSender#1#2#3#4#5#6#7#8{
	\setWWW{#1}
	\def\getSenderKurz{#1}
	\def\getSenderStreet{#2}
	\def\getSenderHNo{#3}
	\def\getSenderBuildNo{#4}
	\def\getSenderCity{#6}
	\def\getSenderPostcode{#5}
	\def\getSenderCountry{\MakeUppercase{#7}}
	\def\getSenderKennziffer{#8}
	}\setSender{}{}{}{}{}{}{}{}
\def\getAnlagen{\ifattached\begingroup\makeatletter\ifnum\value{attCount}>0
		\getAnlagenText~\theattCount
		\begin{itemize}\def\labelitemi{\empty}
			\setcounter{linecnt}{0}
			\openin\myread=\jobname.att
			\@whilesw\unless\ifeof\myread\fi{%
				\stepcounter{linecnt}
				\read\myread to \command%
				\item \command
			}%
			\closein\myread%
		%\ifnum\value{linecnt}=0\item \hfill\fi
		\end{itemize}
		\vspace{-\baselineskip}% latex adds extra line to file, thus there is an extra empty item, thus jump on it!
	\fi
	\if@filesw
		\expandafter\newwrite\csname tf@att\endcsname%
		\immediate\openout \csname tf@att\endcsname \jobname.att\relax%
	\fi%
	\@nobreakfalse
\endgroup\fi}
\def\attach#1{\stepcounter{attCount}\addtocontents{att}{\protect #1}}

\pagestyle{rwthpage}

\def\kontoblock#1#2#3#4#5#6{\raggedright\hfill\newline\hfill\newline\footnotesize#1\hfill\newline#2\hfill\newline\getKontoText~#3\newline\getBLZText~#4\newline\getSWIFTText:~#5\newline\getIBANText:~#6}
\def\taxblock#1#2{\raggedright\footnotesize\getUStIdText\newline\getUStId\newline\hfill\newline\getSteuerText\newline\getSteuerNummer}
\def\mfg#1{}\renewcommand{\mfg}[1][\getSenderName]{\raggedright\noindent\newline\getmfgText\hfill\newline\hfill\newline\hfill\newline\hfill\newline#1\vfill\noindent\getAnlagen\mfgedtrue}
\def\anrede#1{}\renewcommand{\anrede}[1][\getSalutation]{\ifthenelse{\equal{#1}{\empty}}{}{\flushleft{#1\\  \hfill \newline}}} %JB: added missing parentheses
\def\salutation#1{}\renewcommand{\salutation}[1][\getSalutation]{\anrede[#1]}
\def\pagelabel{\footnotesize\thepage/\pageref{LastPage}}
% right date format (w/o datetime for minimal dependencies)
\def\leadingzero#1{\expandafter\ifnum#1<10 0#1\else #1\fi}
\def\RWTHFormatDate#1#2#3{}\renewcommand{\RWTHFormatDate}[3][\year]{\leadingzero{\number#3}.\leadingzero{\number#2}.\number#1}
\def\setDate#1#2#3{}\renewcommand{\setDate}[3][\year]{\renewcommand{\RWTHdate}{\RWTHFormatDate[#1]{#2}{#3}}}
\def\RWTHdate{\RWTHFormatDate[\year]{\month}{\day}}
\AtBeginDocument{\logosystem\sidepanel\footer\windowpanel\ifunblock\raggedright\fi\iffolded\fold\fi%
	% firstpage label
	\ifschmal%
		\begin{textblock}{7}[0,1](158.5,289)%
			\flushleft\pagelabel%
		\end{textblock}%
	\else%
		\begin{textblock}{7}[1,1](202.5,289)%
			\flushright\pagelabel%
		\end{textblock}%
	\fi%
	\ifschmal\enlargethispage{-60mm}\else\enlargethispage{-88mm}\fi
	\getSubject%
	\ifthenelse{\equal{\getpagerefnumber{LastPage}}{1}}{\empty}{%
		\afterpage{\global\setlength{\headheight}{36mm}}%
	}%
}%
\AtEndDocument{%
	\begingroup\label{LastPage}\endgroup%
	\begingroup\ifmfged\empty\else\mfg\fi\endgroup%
	\ifwieskeed\setcounter{page}{0}\newpage\fi%
}%

\def\layoutNumbers{%
\getPhoneText\quad\getPhone\newline%
\ifschmal\ifthenelse{\equal{\getPhoneTwo}{\empty}}{}{\white\getPhoneText\quad\getPhoneTwo\newline}\fi%
\getFaxText\quad\getFax\newline%
\ifschmal\ifthenelse{\equal{\getMobil}{\empty}}{}{\getMobilText\quad\getMobil\newline}\fi\hfill\newline%
}

\def\layoutAdress#1#2#3#4#5#6#7#8#9{\noindent#1\newline%
	\noindent#2\newline%
\noindent#3\newline%
\noindent#4~#5\ifthenelse{\equal{#6}{\empty}}{}{,~\getBuildText~#6}\newline%
\noindent#7~#8\newline%
\noindent\MakeUppercase{#9}%
}

\def\footer{%% footer (if default)
\setcounter{linecnt}{0}
\ifschmal%
	\begin{textblock}{44}[0,1](158.5,284)%
		\noindent\taxblock\getUStId\getSteuerNummer%
		\begingroup%
			\makeatletter%
			\openin\myread=\jobname.acc
			\@whilesw\unless\ifeof\myread\fi{%
				\stepcounter{linecnt}%
				\read\myread to \command%
				\ifnum\value{linecnt}<5\command\fi%
			}%
			\closein\myread%
			\if@filesw
      				\expandafter\newwrite\csname tf@acc\endcsname%
				\immediate\openout \csname tf@acc\endcsname \jobname.acc\relax%
			\fi%
			\@nobreakfalse
		\endgroup%
	\end{textblock}%
\else%
	\begin{textblock}{44}[0,1](20,284)%
		\noindent\taxblock\getUStId\getSteuerNummer\newline%
	\end{textblock}%
	\begingroup%
		\makeatletter%
		\setcounter{linecnt}{21}%
		\openin\myread=\jobname.acc
		\@whilesw\unless\ifeof\myread\fi{%
  			\addtocounter{linecnt}{45}%
			\read\myread to \command%
			\ifnum\value{linecnt}<175
				\begin{textblock}{44}[0,1](\thelinecnt,284)%
				% wegen den newlines im macro, muss das von unten ausgerichtet werden
					\command%
				\end{textblock}%
			\fi%
		}%
		\closein\myread%
		\if@filesw
			\expandafter\newwrite\csname tf@acc\endcsname%
			\immediate\openout \csname tf@acc\endcsname \jobname.acc\relax%
		\fi%
		\@nobreakfalse
	\endgroup%
\fi%
}
\def\fold{%
\begin{textblock}{10}[0,0](0,105)\noindent\blue[50]{\rule{7mm}{1pt}\hfill}\end{textblock}%
\begin{textblock}{10}[0,0](0,148.5)\noindent\blue[50]{\rule{7mm}{1pt}\hfill}\end{textblock}%
\begin{textblock}{10}[0,0](0,210)\noindent\blue[50]{\rule{7mm}{1pt}\hfill}\end{textblock}%
}
\def\sidepanel{%
	% seitenfeld
	\ifschmal%
	\begin{textblock}{44}[1,0](202.5,36)%
		\raggedright\small\noindent\textbf\getDeanFullName\newline\getDeanFunction\hfill\newline%
\textbf\getSenderFullName\newline\getSenderFunction\hfill\newline%
\getSenderStreet~\getSenderHNo%\ifthenelse{\equal{\getSenderBuildNo}{\empty}}{}{,~\getBuildText~\getSenderBuildNo}
\newline%
\getSenderPostcode~\getSenderCity\newline%
\MakeUppercase{\getSenderCountry}\newline%
\hfill\newline
\ifthenelse{\equal{\getSenderBuildNo}{\empty}}{}{\getBuildText~\getSenderBuildNo}\hfill\newline%
\ifthenelse{\equal{\getFloorNo}{\empty}}{}{\getFloorText~\getFloorNo,~}%
\ifthenelse{\equal{\getRoomNo}{\empty}}{}{\getRoomText~\getRoomNo}%
\ifthenelse{\equal{\getFloorNo\getRoomNo}{\empty}}{}{\hfill\newline}%
\hfill\newline\layoutNumbers%
\getEMail\hfill\newline\getWWW\newline\hfill\newline%
\ifthenelse{\equal{\getSignature}{\empty}}{\newline}{\getSignatureText~\getSignature\newline}%
\ifprintdate\textbf{\RWTHdate}\fi%
	\end{textblock}
	\else\begin{textblock}{60}[1,0](202.5,36)%
		\raggedright\small\noindent\textbf\getDeanFullName\newline\getDeanFunction\hfill\newline%
\textbf\getSenderFullName\newline\getSenderFunction\hfill\newline%
\getSenderStreet~\getSenderHNo\ifthenelse{\equal{\getSenderBuildNo}{\empty}}{}{,~\getBuildText~\getSenderBuildNo}\newline%
\getSenderPostcode~\getSenderCity\newline%
\MakeUppercase{\getSenderCountry}\newline%
\layoutNumbers\getEMail\newline\hfill\newline%
\ifthenelse{\equal{\getInvoiceNumber}{\empty}}{\newline\hfill\newline}{\getInvoiceNumberText~\getInvoiceNumber\newline\hfill\newline}%
%\getInvoiceNumberText~\getInvoiceNumber\newline\hfill\newline%
\ifthenelse{\equal{\getSignature}{\empty}}{\newline}{\getSignatureText~\getSignature\newline}%
%\getSignatureText~\getSignature\newline%
\ifprintdate\textbf{\RWTHdate}\fi%
	\end{textblock}\fi
}
\def\logosystem{%
		% logo mit bar
	\begin{textblock}{1}[0,0](137.3,4)%
\noindent\blue[25]{\vrule width 1pt height 80mm }
	\end{textblock}
	\begin{textblock}{150}[1,1](207.5,36)%
\noindent\flushright\noindent%
\IfFileExists{\getLogo}{\includegraphics[height=32mm]{\getLogo}}{Logo not found. Check path and filename.\\ \vfill}% logos kommen mit 32mm hoehe
	\end{textblock} 
}
\def\windowpanel{%
	\begin{textblock}{85}[0,0](20,45)\raggedright\noindent{\scriptsize\blue{{\bfseries\getSenderKurz}~~\textbar~~\getSenderStreet~~\getSenderHNo~~\textbar~~\getSenderPostcode~~\getSenderCity~~\textbar~~\getSenderCountry} \hfill  \getSenderKennziffer}\newline\getRemark\newline%
		\layoutAdress{\getHonorific}{\getFirm}{\getContact}{\getStreet}{\getHNo}{\getBuildNo}{\getPostcode}{\getCity}{\getCountry}	
	\end{textblock}
}
