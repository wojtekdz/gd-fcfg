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
from gaelicProc import *

def parseNow():
    """Parse sentences from sentences.txt with preprocessing and postprocessing, printing them out one by one

    Arguments: none
    Returns: none, prints out list of trees

    """

    grammar = nltk.data.load('file:gaelic.fcfg')
    cp = nltk.FeatureChartParser(grammar)

    #[DEL] to check how these things line up
    print grammar

    sentences = gaelicProc.preprocessSentences('sentences.txt')


    for sentence in sentences:
        print '\n' + gaelicProc.postprocessSentences(sentence) #print out reverted orthographic form of the sentence
        trees = cp.nbest_parse(sentence.split())
        if not trees: print 'CHA GHABH AN ROSGRANN PARSADH'
        else:
            for tree in trees:
                #[TODO] how to print a Tree in utf8?
                #THIS DOES NOT WORK BECAUSE IT CAN ONLY ENCODE A STRING: print unicode(tree, 'utf8')
                #THIS DOES NOT WORK BECAUSE Tree OBJECT DON'T HAVE A METHOD ENCODE: print tree.encode('utf8')
                print tree
                #print tree.draw()

compileGrammar()
generateMultiwords()
parseNow()
