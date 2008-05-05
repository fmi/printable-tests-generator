# -*- coding: utf-8 -*-
import latex
import string

class LatexAnswersWriter(latex.LatexTestWriter):
	letters = (u'А', u'Б', u'В', u'Г', u'Д', u'Е')
	def correctLetter(self, q):
		correct = None
		for (l, a) in zip(self.letters, q.answers):
			if a.correct:
				if correct: correct = u'+'
				else: correct = l
		return correct
	def write(self, test, f=None):
		self.setFD(f)
		body = ''
		header = self.whole(test)
		res = self.verbatise(string.Template(header).substitute(body=body))
		numquestions = len(test.questions)
		# DIRTY!
		tabspaces =  u' & '.join([r' ']*numquestions)
		print test.questions
		tabanswers = u' & '.join([self.correctLetter(q) for q in test.questions])
		#res = res.replace(tabspaces, tabanswers+r' \\'+'\n'+r'\hline'+'\n'+tabspaces)
		res = res.replace(tabspaces, tabanswers)
		res = self.hackUniLits(res)
		print >>self.f, res.encode('utf-8')
