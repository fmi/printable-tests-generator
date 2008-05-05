# -*- coding: utf-8 -*-

from xml.dom import minidom

import getopt
import os
import os.path
import re
import sys
import string
import latex
import latexanswers
from defs import Struct

QUESTION_TAG = u"q"
QUESTION_TEXT_TAG = u"text"
ANSWER_TAG = u"a"
PRE_TAG = u"pre"
CODE_TAG = u"code"
CORRECT_ATTRIBUTE = u"correct"
CORRECT_ATTRIBUTE_VALUE = u"true"
STRONG_TAG = u"strong"

class ParseError(Exception): pass

class XMLTestReader:
	"""Reads questions from an XML file"""

	def _d(self, s):
		if self._debug:
			print "Debug: %s" % s

	def __init__(self, source):
		self.source = source
		self._debug = False
		self._questions = None

	def __call__(self):
		return self.getQuestions()

	def _load(self):
		if isinstance(self.source, basestring):
			self.f = open(self.source)
		else:
			self.f = self.source
		xmldoc = minidom.parse(self.f).documentElement
		self.f.close()
		return xmldoc

	def getQuestions(self):
		if self._questions == None:
			self._questions = map(self.handleQuestion, self._load().getElementsByTagName(QUESTION_TAG))
		return self._questions



	def handleQuestion(self, node):
		self._d("handleQuestion: %s" % node.tagName)
		res = Struct()
		res.text = self.handleQuestionText(node.getElementsByTagName(QUESTION_TEXT_TAG))
		if not res.text:
			return False
		self._d("Question text: %s" % res.text)
		res.answers = map(self.handleAnswer, node.getElementsByTagName(ANSWER_TAG))
		if not res.answers: raise ParseError("The questions must have at least one answer!")
		return res
			


	def handleQuestionText(self, nodes):
		if len(nodes) != 1:
			raise ParseError("A question must have exacly one text!")
		text = self.verbatise(nodes[0])
		self._d("Question text: %s" % text)
		return text
	
	def handleAnswer(self, node):
		answer = Struct()
		correctAttr = node.attributes.get(CORRECT_ATTRIBUTE)
		answer.correct =  correctAttr and (correctAttr.nodeValue == CORRECT_ATTRIBUTE_VALUE)
		answer.text = self.verbatise(node)
		return answer


	def verbatise(self, node):
		self._d("Verbatise: %s" % node.nodeName)
		return u''.join(map(self.verbatiseNode, node.childNodes))


	def verbatiseNode(self, node):
		self._d('verbatizing...')
		if node.nodeType == node.TEXT_NODE:
			return unicode(node.data)
		if node.nodeType == node.ELEMENT_NODE:
			tagName = node.tagName
			if tagName == STRONG_TAG:
				tmpl = u"*%s*"
			elif tagName == PRE_TAG:
				tmpl = u"<pre>%s</pre>"
			elif tagName == CODE_TAG:
				tmpl = u"<code>%s</code>"
			else:
				tmpl = u"<%s>%%s</%s>" % unicode(tagName)
			inside = ''.join(map(self.verbatiseNode, node.childNodes))
			return tmpl % inside
		return ''
