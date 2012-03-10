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
import gaelicProc
import codecs
from gaelicProc import *

def parseNow():
    """Parse sentences from sentences.txt with preprocessing and postprocessing, printing them out one by one

    Arguments: none
    Returns: none, prints out list of trees

    """
    #[TODO] TRY AND FIX THIS WHEN THESIS IS IN: THIS ATTEMPTS TO CREATE A FEATURE GRAMMAR IN UTF8 - BUT IS GIVING PARSE ERRORS IN NLTK.GRAMMAR
    #grammar = nltk.grammar.parse_fcfg(codecs.open('gaelic.fcfg', 'rb', encoding='utf8').read())

    #THIS WORKS BUT WITHOUT THE UTF8 ENCODING
    grammar = nltk.data.load('file:gaelic.fcfg')
    cp = nltk.FeatureChartParser(grammar)

    #print grammar

    sentences = gaelicProc.preprocessSentences('sentences.txt')

    for sentence in sentences:
        print '\n' + gaelicProc.postprocessSentences(sentence) #print out reverted orthographic form of the sentence
        trees = cp.nbest_parse(sentence.split())
        if not trees: print 'CHA GHABH AN ROSGRANN PARSADH.'
        else:
            for tree in trees:
                print tree
                #print tree.draw()

compileGrammar()
generateMultiwords()
parseNow()
