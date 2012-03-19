# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        CONTEXT-FREE FEATURE-BASED GRAMMAR FOR GAELIC
# Purpose:     Parsing Gaelic learners' sentences up to intermediate level
#
# Author:      Wojtek Dziejma, supervised by Mark McConville
#
# Created:     2011-12
# Copyright:   (c) Wojtek Dziejma 2012
# Licence:     GPLv3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import nltk.parse
import nltk.grammar
import nltk.data
import nltk.draw
import codecs

#[TODO] WHY DO YOU NEED BOTH DECLARATIONS TO RUN YOUR OWN MODULES? READ THE PYTHON DOCS.
import gaelicProc
from gaelicProc import *

import gaelicTest
from gaelicTest import *

def parseNow(sentence_file):
    """Parse sentences from sentences.txt with preprocessing and postprocessing, printing them out one by one

    Arguments: none
    Returns: none, prints out list of trees

    """
    #[TODO] THIS ATTEMPTS TO CREATE A FEATURE GRAMMAR IN UTF8 - BUT IS GIVING PARSE ERRORS IN NLTK.GRAMMAR
    #grammar = nltk.grammar.parse_fcfg(codecs.open('gaelic.fcfg', 'rb', encoding='utf8').read())

    #THIS WORKS BUT WITHOUT THE UTF8 ENCODING
    grammar = nltk.data.load('file:gaelic.fcfg')
    cp = nltk.FeatureChartParser(grammar)

    sentences = gaelicProc.preprocessSentences(sentence_file)

    for sentence in sentences:
        print filterOrthography(sentence)
        rev = '\n' + gaelicProc.postprocessSentences(sentence) #or add .decode('utf8') if that's desired, the trees print in ASCII on a PC anyway
        print rev #print out reverted orthographic form of the sentence
        trees = cp.nbest_parse(sentence.split())
        if not trees: print 'CHA GHABH AN ROSGRANN PARSADH.'
        else:
            for tree in trees:
                    print tree
                    # DRAW A GRAPHICAL TREE USING TKINTER
                    #print tree.draw()


compileGrammar()
generateMultiwords()

#testParse('tests/irreg_verbs_ACCEPT.txt')
#testParse('tests/irreg_verbs_REJECT.txt')

#testParse('tests/nouns_ACCEPT.txt')
#testParse('tests/nouns_REJECT.txt')

parseNow('sentences.txt')
