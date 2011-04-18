#  -*-  coding: utf-8 -*-
import sys
import os
import os.path
from os.path import join, realpath
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
        raise Exception('Usage %s <variant>' % sys.argv[0])
    d = realpath('/Users/nb/github/fmi/python-quizzes/10-11')
    files = [join(d, f) for f in os.listdir(d) if f.endswith('.txt')]
    counts = ["all"]*len(files)
    spec = dict(zip(files, counts))
    #raise str(spec)
    for var in sys.argv[1:]:
        l = Writer()
    	la = AnswersWriter()	    
    	t = Test(date=u'19.04.2011г.', title=u'Програмиране с Python', subtitle=ur'Тест \No1, Вариант '+var)
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
