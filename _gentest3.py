#!/usr/bin/python2.5
#  -*-  coding: utf-8 -*-
import sys
import os
import os.path
import random

from buildFromTex import main as build

from lib.xmlreader import XMLTestReader
from lib.latex import LatexTestWriter
from lib.latexanswers import LatexAnswersWriter
from lib.defs import Test
from lib.testgen import genTest, loadQuestions

def main():
	# test variant
	if len(sys.argv) > 1:
		var = sys.argv[1]
	else:
		raise Exception('Usage test2gen.py <variant>')
	spec = {
			'test2/questions/sample.xml': 2,
	}
	l = LatexTestWriter()
	la = LatexAnswersWriter()
	t = Test(date=u'25.04.2007г.', title=u'Програмиране с Python', subtitle=ur'Тест \No1, Вариант '+var)
	t.questions = genTest(spec, XMLTestReader)
	if not os.path.isdir('test2/'+var): os.mkdir('test2/'+var)
	tex = open('test2/%s/%s.tex' % (var, var), 'w')
	texAns = open('test2/%s/%s-answers.tex' % (var, var), 'w')
	l.write(t, tex)
	la.write(t, texAns)
	tex.close()
	texAns.close()
	build(var, 'test2/'+var, 'test2/'+var)
if __name__ == "__main__":
	main()
