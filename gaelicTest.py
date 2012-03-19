# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        TEST SUITE for GAELIC FCF GRAMMAR
# Purpose:     Testing words with other modules in the Gaelic package
#
# Author:      Wojtek Dziejma, supervised by Mark McConville
#
# Created:     2011-12
# Copyright:   (c) Wojtek Dziejma 2012
# Licence:     GPLv3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import gaelicOps
import gaelicProc
import nltk.parse
import nltk.grammar
import nltk.data

words = ["toilichte", "spòrsail", "cudromach", "beag", "àrd"]

def testOps(words):
    """Test individual words for lenition and slenderization results

    Arguments: none
    Returns: none, prints out list operation results

    """
    for word in words:
        print "\n WORD: %s \n LEN: %s \n SDR: %s" % (word, gaelicOps.lenite(word), gaelicOps.slenderize(word))

def testParse(sentence_file):
    """Parse sentences from sentences.txt with preprocessing and postprocessing, printing them out one by one

    Arguments: none
    Returns: none, prints out list of trees

    """
    grammar = nltk.data.load('file:gaelic.fcfg')
    cp = nltk.FeatureChartParser(grammar)

    sentences = gaelicProc.preprocessSentences(sentence_file)


    parse_errors = []
    single_parses = []
    multiple_parses = 0

    print "\n\n" + sentence_file

    for sentence in sentences:
        trees = cp.nbest_parse(sentence.split())

        if not trees:
            parse_errors = parse_errors + [sentence] #track parse errors
        else:
            if len(trees) > 1: #report sentences with multiple parses
                print '\n' + gaelicProc.postprocessSentences(sentence).decode("utf8") #print out reverted orthographic form of the sentence
                for tree in trees:
                    print tree
                multiple_parses += 1
            else:
                single_parses = single_parses + [sentence] #track parse successes

    if multiple_parses == 0:
        print "CHA ROBH ROSGRAINN LE BARRACHD IS 1 TORADH PARSAIDH ANN"
    else:
        print "BARRACHD IS 1 TORADH PARSAIDH: " + str(multiple_parses)

    #report parse statistics
    print "\nROSGRAINN UILE: " + str(len(sentences))

    #display sentences with single parses
    print "\n1 TORADH PARSAIDH A-MHÀIN: " + str(len(single_parses))
    for sentence in single_parses:
        print gaelicProc.postprocessSentences(sentence).decode("utf8")

    #display sentences with parse errors
    print "\nCHA GHABH PARSADH: " + str(len(parse_errors))
    for sentence in parse_errors:
        print gaelicProc.postprocessSentences(sentence).decode("utf8")