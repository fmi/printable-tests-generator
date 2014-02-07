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
    if len(sys.argv) > 2:
        questions_path = sys.argv[1]
    else:
        raise Exception('Usage %s <path-to-folder-with-questions> <variant> [<variant> ...]' % sys.argv[0])

    # questions_path = realpath('/Users/dimitardimitrov/Projects/web/ruby-homework-hidden/ruby-quizzes/11-12')
    files = [join(questions_path, f) for f in os.listdir(questions_path) if f.endswith('.txt')]
    counts = ["all"] * len(files)
    spec = dict(zip(files, counts))

    for variant in sys.argv[2:]:
        l = Writer()
        la = AnswersWriter()
        t = Test(date=u'05.12.2011 г.', title=u'Програмиране с Ruby', subtitle=ur'Тест \No1, Вариант '+variant)
        t.questions = genTest(spec, Reader, reorder_answers=False)
        if not os.path.isdir(join(questions_path, variant)): os.mkdir(join(questions_path, variant))
        tex = open(join(questions_path, '%s/%s.tex') % (variant, variant), 'w')
        texAns = open(join(questions_path, '%s/%s-answers.tex') % (variant, variant), 'w')
        l.write(t, tex)
        la.write(t, texAns)
        tex.close()
        texAns.close()
        build(variant, join(questions_path, variant),  join(questions_path, variant))

if __name__ == "__main__":
    main()
