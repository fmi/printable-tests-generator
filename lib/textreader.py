# -*- coding: utf-8 -*-
import getopt
import os
import os.path
import re
import sys
import string
import codecs

import latex
import latexanswers
from defs import Struct, Test

#TODO: add file name/line to parse errors

class ParseError(Exception): pass

class TextTestReader:
	"""Reads questions from a text source (directory)"""

	def _d(self, s):
		if self._debug:
			print "Debug: %s" % s

	def __init__(self, source):
		self.source = source
		self._debug = False

	def __call__(self):
		return self.getQuestions()

	def getQuestions(self):
		if isinstance(self.source, basestring):
			self.f = codecs.open(self.source, "r", "utf-8")
		else:
			self.f = self.source
		return list(self.ireadQuestions())

	def getDirQuestions(self):
		questions = []
		for x in os.listdir(source):
			if os.path.isdir(x):
				if self.ecurse: continue
				#TODO recurse
			elif os.listdir.isfile(x):
				self.f = open(os.path.join(x))
				questions.extend(list(self.ireadQuestions()))

				
	def ireadQuestions(self):
		while True:
			q = self.readQuestion()
			if not q: break
			yield q
		
	def readQuestion(self):
		res = Struct()
		res.text = self.readQuestionText()
		if not res.text:
			return False
		res.text = self.verbatise(res.text)
		res.answers = list(self.ireadAnswers())
		if not res.answers: raise ParseError("The questions must have at least one answer!")
		return res
			


	def readQuestionText(self):
		txt = u''
		openBacktick = 0
		while(True):
			l = self.f.readline()
			if not l: break
			l = l.rstrip()
			self._d('Question text-line read: %s' % l)
			if not openBacktick and (not l or l.isspace()):
				if txt: return txt
				else: continue # skip empty lines before the question text
			if not openBacktick and l[0].isspace():
				if l.lstrip()[0] in (u'*', u'+'): raise ParseError("There must be an empty line between the question and its answers!")
				raise ParseError("Lines of question text cannot start with whitespace!")
			openBacktick = (l.count(u'`') + openBacktick)%2
			txt += l+'\n'
		return txt
	
	def ireadAnswers(self):
		while True:
			a = self.readAnswer()
			if not a: break
			yield a

	def readAnswer(self):
		"""Just for now answers could be at most one line!"""
		answer = Struct()
		l = self.f.readline().rstrip()
		self._d("Answer-line read: %s" % l)
		if not l:
			return None
		match = re.match("\s+(\*|\+)\s*(\S.*)", l)
		if match:
			if u'+' == match.group(1): answer.correct = True
			else: answer.correct = False
			answer.text = match.group(2)
			answer.text = self.verbatise(answer.text)
			return answer
		else:
			raise ParseError("Answers must begin with whitespace, followed by a + or a *! Line is "+l)

	def verbatise(self, s):
		self._d('verbatizing...')
		openBacktick = False
		lnews = []
		for line in s.split('\n'):
			self._d('Line: '+line)
			news = u''
			first = line.find(u'`')
			last = line.rfind(u'`')
			self._d('First and last ticks: %d %d' % (first, last))
			for (i, c) in enumerate(line):
				if u'`' == c:
					if i == first:
						if openBacktick:
							news += ur'</pre>'
							openBacktick = False
						elif i != last:
							news += ur'<code>'
							openBacktick = True
						else:
							news += ur'<pre>'
							openBacktick = True
					elif i == last:
						if openBacktick:
							news += ur'</code>'
							openBacktick = False
						else:
							news += ur'<pre>'
							openBacktick = True
					else:
						if openBacktick:
							news += ur'</code>'
							openBacktick = False
						else:
							news += u'<code>'
							openBacktick = True
				else:
					news += c
			lnews.append(news)
		return ('\n'.join(lnews)).rstrip()


				
def main():
	l = latex.LatexTestWriter()
	la = latexanswers.LatexAnswersWriter()
	t = Test(date='21.04.2007г.', title='Програмиране с Python', subtitle='Тест \No1, Вариант \No1')
	ttr = TextTestReader('q.txt')
	t.questions = ttr.getQuestions()
	l.write(t, 'real.tex')
	la.write(t, 'reala.tex')


		

if __name__ == "__main__":
	main()
