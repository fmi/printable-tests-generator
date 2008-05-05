# -*- coding: utf-8 -*-
import sys
import string
import re

class LatexTestWriter:
	def setFD(self, f=None):
		if not f:
			self.f = sys.stdout
		elif isinstance(f, basestring):
			self.f = open(f, 'w')
		else:
			self.f = f


	def texify(self, s):
		print repr(s)
		s = re.sub(ur'\*(\S+)\*', r'\\underline{\\textbf{\1}}', s)
		s = s.replace(u'->', u'$\\to$')
		return s

	def write(self, test, f=None):
		self.setFD(f)
		body = self.questions(test.questions)
		header = self.whole(test)
		verbatised = self.verbatise(string.Template(header).substitute(body=body))
		verbatised = self.hackUniLits(verbatised)
		print >>self.f, verbatised.encode('utf-8')
		
	def verbatise(self, s):
		s = s.replace(u'<code>', ur'\verb|')
		s = s.replace(u'</code>', ur'|')
		s = s.replace(u'<pre>', ur'\begin{verbatim}')
		s = s.replace(u'</pre>', ur'\end{verbatim}')
		return s

	def hackUniLits(self, s):
		return s.replace(r'\\u', r'\u')

	def whole(self, test):
		tmpl = ur"""\documentclass[a4paper,10pt]{article}
\\usepackage[T2A]{fontenc}
\\usepackage[cp1251]{inputenc}
\\usepackage[bulgarian]{babel}
\\usepackage[left=2cm,top=2cm,right=2cm,bottom=2cm]{geometry}
\begin{document}

\begin{center}
\huge{$title} \\
\LARGE{$subtitle} \\
\Large{$date}
\end{center}
\vspace{0.5cm}
\begin{tabular}{ll}
\large{Факултетен номер:}\hspace{3cm} & \large{Име:}
\end{tabular}
\vspace{0.5cm}

%Place for answers%
\begin{tabular}[c]{$tabspecifier}
\hline

$tabnumbers \\
\hline
$tabspaces \\
\hline
\end{tabular}

$body

\end{document}
"""
		numquestions = len(test.questions)
		tabspecifier = u'|'+u'|'.join([u'p{0.2cm}']*numquestions)+u'|'
		tabnumbers = u' & '.join(map(str, range(1, numquestions+1)))
		tabspaces =  u' & '.join([u' ']*numquestions)
		d = vars()
		d.update(vars(test))
		res = string.Template(tmpl).safe_substitute(d)
		return res

	def questions(self, questions):
		tmpl = ur"""
%Questions start here%
\begin{enumerate}
\renewcommand{\labelenumii}{\Alph{enumii}.}

$sq

\end{enumerate}
"""
		qt = ur"""
%\begin{samepage}%

\item $text

\begin{enumerate}

$sa

\end{enumerate}

%\end{samepage}%"""
		sq = []
		for q in questions:
			q.text = self.texify(q.text)
			q.sa = u'\n'.join([u'\\item '+self.texify(a.text) for a in q.answers])
			sq.append(string.Template(qt).substitute(vars(q)))
		sq = u'\n'.join(sq)
		return string.Template(tmpl).substitute(sq=sq)
