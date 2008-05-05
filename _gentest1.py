#!/usr/bin/python2.5
#  -*-  coding: utf-8 -*-
import sys
import random

from buildFromTex import main as build

from lib.latex import LatexTestWriter
from lib.latexanswers import LatexAnswersWriter
from lib.defs import Test
from lib.testgen import genTest, loadQuestions

def main():
	# test variant
	if len(sys.argv) > 1:
		var = sys.argv[1]
	else:
		var = 'ham'
	spec = {
			'test1/1-basic.txt': 4, # 12
			'test1/2-builtintypes.txt': 4, # 19
			'test1/3-func.txt': 4, # 15
			'test1/4-modules.txt': 2, # 5
			'test1/5-classes.txt': 4, # 13
			'test1/6-exceptions.txt': 2, # 8
			'test1/7-iter.txt': 3, # 9
			'test1/unsorted.txt': 2,
	}
	l = LatexTestWriter()
	la = LatexAnswersWriter()
	t = Test(date='25.04.2007г.', title='Програмиране с Python', subtitle=r'Тест \No1, Вариант '+var)
	t.questions = genTest(spec, '.txt')
	tex = open('%s.tex' % var, 'w')
	texAns = open('%s-answers.tex' % var, 'w')
	l.write(t, tex)
	la.write(t, texAns)
	tex.close()
	texAns.close()
	build(var)
if __name__ == "__main__":
	main()
