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
        #this is where the first-pass correction could be applied i.e. sentence = filterOrthography(sentence)
        rev = '\n' + gaelicProc.postprocessSentences(sentence) #or add .decode('utf8') if that's desired, the trees print in ASCII on a PC anyway
        print rev #print out reverted orthographic form of the sentence
        trees = cp.nbest_parse(sentence.split())
        if not trees: print 'CHA GHABH AN ROSGRANN PARSADH.'
        else:
            for tree in trees:
                    print tree
                    # DRAW A GRAPHICAL TREE USING TKINTER
                    #print tree.draw()

def toyparse(type):
    if type == "CFG":

        grammar = nltk.parse_cfg("""
                % start S
                S -> V NP A
                NP -> DET N
                V -> "tha"
                DET -> "an" | "a'"
                N -> "cù" | "chù"
                A -> "sgìth"
                """)
        cp = nltk.ChartParser(grammar)

    elif type == "FCFG":
        grammar = nltk.parse_fcfg("""
                % start S
                S[TYPE=statement]-> V[TYPE=sub, TENSE=pres] NP[CASE=rad] A[TYPE=pred]
                NP[CASE=?x] -> DET[CASE=?x, GEN=?y] N[CASE=?x, GEN=?y]
                V[TYPE=sub, TENSE=pres] -> "tha"
                DET[GEN=masc, CASE=rad] -> "an"
                DET[GEN=masc, CASE=prep] -> "a'"
                N[GEN=masc, CASE=prep] -> "chù"
                N[GEN=masc, CASE=rad] -> "cù"
                A[TYPE=pred] -> "sgìth"
        """)
        cp = nltk.FeatureChartParser(grammar)

    trees = cp.nbest_parse("tha an cù sgìth".split())
    if not trees: print 'CHA GHABH AN ROSGRANN PARSADH.'
    else:
        for tree in trees: print tree

compileGrammar()
generateMultiwords()

#testParse('tests/verbs_ACCEPT.txt')
#testParse('tests/verbs_REJECT.txt')

#testParse('tests/nouns_ACCEPT.txt')
#testParse('tests/nouns_REJECT.txt')

parseNow('sentences.txt')
#toyparse("CFG")
#toyparse("FCFG")

