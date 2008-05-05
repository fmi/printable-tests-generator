import sys
import os
from os.path import join

def main(var, texdir='.', outdir='.'):
	""" Builds dvi, ps and pdf files from a given tex of a test"""

	if not os.path.isdir(outdir): os.mkdir(outdir)
	inTexFile = join(texdir, '%s.tex' % var)
	outTexFile = join(outdir, '%s-cp.tex' % var)
	inTexAnswersFile = join(texdir, '%s-answers.tex' % var)
	outTexAnswersFile = join(outdir, '%s-answers-cp.tex' % var)
	# convert to cp1251
	os.system("iconv -f utf-8 -t cp1251 %s > %s" % (inTexFile, outTexFile))
	os.system("iconv -f utf-8 -t cp1251 %s > %s" % (inTexAnswersFile, outTexAnswersFile))
	os.chdir(outdir)
	# actually build the dvis
	os.system("latex %s-cp.tex" % var)
	os.system("latex %s-answers-cp.tex" % var)
	# get rid of the cp suffix
	os.rename("%s-cp.dvi" % var, "%s.dvi" % var)
	os.rename("%s-answers-cp.dvi" % var, "%s-answers.dvi" % var)
	# build the fancy files: ps and pdf
	os.system("dvips %s.dvi" % var)
	os.system("dvips %s-answers.dvi" % var)
	os.system("ps2pdf %s.ps" % var)
	os.system("ps2pdf %s-answers.ps" % var)

if __name__ == "__main__":
	main(sys.argv[1])
