#!/usr/bin/python2.5
#  -*-  coding: utf-8 -*-
import sys
import os
import os.path
from os.path import join
import random

from buildFromTex import main as build

from lib.textreader import TextTestReader as Reader
from lib.latex import LatexTestWriter as Writer
from lib.latexanswers import LatexAnswersWriter as AnswersWriter
from lib.defs import Test
from lib.testgen import genTest, loadQuestions

def main():
	# test variant
	if len(sys.argv) > 1:
		var = sys.argv[1]
	else:
		raise Exception('Usage test4gen.py <variant>')
	d = 'test4'
	files = "1-basic.txt  2-builtintypes.txt  3-func.txt  4-modules.txt  5-re.txt  6-files-unicode.txt  7-classes.txt  8-exceptions.txt".split()
	files = [join(d, f) for f in files]
	counts = ["all"]*8
	spec = dict(zip(files, counts))
	l = Writer()
	la = AnswersWriter()
	t = Test(date=u'07.05.2008г.', title=u'Програмиране с Python', subtitle=ur'Тест \No1, Вариант '+var)
	t.questions = genTest(spec, Reader, reorder_answers=False)
	if not os.path.isdir(join(d, var)): os.mkdir(join(d, var))
	tex = open(join(d, '%s/%s.tex') % (var, var), 'w')
	texAns = open(join(d, '%s/%s-answers.tex') % (var, var), 'w')
	l.write(t, tex)
	la.write(t, texAns)
	tex.close()
	texAns.close()
	build(var, join(d, var),  join(d, var))
if __name__ == "__main__":
	main()
