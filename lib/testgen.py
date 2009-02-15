#!/usr/bin/python2.5
#  -*-  coding: utf-8 -*-
import sys
import os
import os.path
import latex
import latexanswers
import random
from defs import Test

def genTest(spec, reader, reorder_answers = True):
		"""Spec is a dictionary file -> count, var is the name of the test"""
		questions = []
		for item in spec:
			item_questions = loadQuestions(item, reader, reorder_answers)
			if 'all' != spec[item]:
				item_questions = random.sample(item_questions, spec[item])
			questions.extend(item_questions)
		return questions

def loadQuestions(item, reader, reorder_answers = True):
	if os.path.isfile(item):
		ttr = reader(item)
		questions = ttr.getQuestions()
		for q in questions:
			if reorder_answers: random.shuffle(q.answers)
		return questions
	else:
		raise IOError(item+" is not a valid question file!")

