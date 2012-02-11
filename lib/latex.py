# -*- coding: utf-8 -*-
from __future__ import division
import sys
import math
import string
import re

class LatexTestWriter:
	
	letters = (u'А', u'Б', u'В', u'Г', u'Д', u'Е', u'Ж', u'З', u'И', u'Й', u'К', u'Л', u'М', u'Н', u'О', u'П', u"Р", u"С", u"Т", u"У", u"Ф", u"Х", u"Ц", u"Ш", u"Щ", u"Ъ", u"Ь", u"Ю", u"Я")
	
	def setFD(self, f=None):
		if not f:
			self.f = sys.stdout
		elif isinstance(f, basestring):
			self.f = open(f, 'w')
		else:
			self.f = f


	def texify(self, s):
		s = re.sub(ur'\*(\S+)\*', r'\\underline{\\textbf{\1}}', s)
		# s = s.replace(u'->', u'$\\to$')
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

	def correctLetter(self, q):
		correct = None
		for (l, a) in zip(self.letters, q.answers):
			if a.correct:
				if correct: correct = u'+'
				else: correct = l
		return correct

	def whole(self, test, answer_sheet = False):
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

$answers

$body

\end{document}
"""
		answers = self.answers(test, len(test.questions), answer_sheet)
		d = vars()
		d.update(vars(test))
		res = string.Template(tmpl).safe_substitute(d)
		return res
		
	def answers(self, test, number, correct_answers = False):
		columns_count = 15
		rows_count = int(math.ceil(number / columns_count))
		answers_tmpl = r"""%Place for answers%
\begin{tabular}[c]{$tabspecifier}
\hline
$rows
\end{tabular}
"""
		row_tmpl = r"""$tabnumbers \\
\hline
$tabletters \\
\hline"""
		rows = []
		tabspecifier = u'|'+u'|'.join([u'p{0.2cm}']*columns_count)+u'|'
		if correct_answers:
			answers = [self.correctLetter(q) for q in test.questions]
		else:
			answers = [u' '] * number
		if number % columns_count != 0: answers.extend([u' '] * (columns_count * rows_count - number))
		for line in xrange(0, rows_count):
			start, end = line*columns_count + 1, line*columns_count + columns_count
			tabnumbers = u' & '.join([str(i) if i <= number else u' ' for i in xrange(start, end + 1)])
			tabletters =  u' & '.join(answers[start-1:end])
			rows.append(string.Template(row_tmpl).safe_substitute(vars()))
		rows = '\n'.join(rows)
		return string.Template(answers_tmpl).safe_substitute(vars())

	def questions(self, questions):
		tmpl = ur"""
%Questions start here%
\begin{enumerate}
\renewcommand{\labelenumii}{\Alph{enumii}.}

$sq

\end{enumerate}
"""
		qt = ur"""
\begin{samepage}

\item $text

\begin{enumerate}

$sa

\end{enumerate}

\end{samepage}
\pagebreak[1]
"""
		sq = []
		for q in questions:
			q.text = self.texify(q.text)
			q.sa = u'\n'.join([u'\\item '+self.texify(a.text) for a in q.answers])
			sq.append(string.Template(qt).substitute(vars(q)))
		sq = u'\n'.join(sq)
		return string.Template(tmpl).substitute(sq=sq)
