# -*- coding: utf-8 -*-
import latex
import string

class LatexAnswersWriter(latex.LatexTestWriter):

	def write(self, test, f=None):
		self.setFD(f)
		body = ''
		header = self.whole(test, answer_sheet = True)
		res = self.verbatise(string.Template(header).substitute(body=body))
		res = self.hackUniLits(res)
		print >>self.f, res.encode('utf-8')
