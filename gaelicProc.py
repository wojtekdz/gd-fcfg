# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        PROCESSOR FOR GAELIC GRAMMAR
# Purpose:     Generating and compiling FCFG productions, pre- and post- processing sentences for the NLTK parser
#
# Author:      Wojtek Dziejma, supervised by Mark McConville
#
# Created:     2011-12
# Copyright:   (c) Wojtek Dziejma 2012
# Licence:     GPLv3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import re
import codecs
from gaelicOps import *

prespace_tokens = ["!", ".", "?"] #these strings will be preprocessed to separate them as tokens with a space BEFORE them
postspace_tokens = ["n-", "h-", "t-"] #and these with a space AFTER them
def filterOrthography(sent):
    print "filtering..."
    return False
    #[TODO] WRITE FUNCTIONS FOR THE LENIENT TOLERATION OF EMPTY AREL, DELENITED BUT INCLUDE DELENITED VERSION DIRECTLY IN THE PRODUCTIONS
    #TWO SOLUTIONS
    #REL -> S[+POL] BUT NOT GOOD BECAUSE WILL LICENCE NON-QUESTION RELATIVE PHRASES WITHOUT AREL
    #PREPROCESS SENTENCES TO FILL IN IMPORTANT SYNTACTIC MARKERS OMMITED IN SPEECH AND THUS SPELLING, BUT LIKELY PROBLEMS WITH CONTEXT: WOULD WORK FOR dè -> dè a BUT MORE DIFFICULT WITH a athair vs a h-athair



def stripList(lst):
    """Remove comments, blank lines etc. from a list of productions read from a file

    """
    lst_stripped = []
    for item in lst:
        if not(item.startswith('#') or item.startswith('\r\n') or item.startswith('\n') or len(item) == 0): #the \r\n is for non-Win filesystems
            lst_stripped = lst_stripped + [item]
    return lst_stripped



def saveToFile(productions, label, filename):
    """Save a productions list to a file, one per line, with a suitable comment label at the start

        Arguments:
            productions (list) - the content
            label (string) - comment to go into the start of the file
            filename (string) - destination file
        Returns: none, writes to file
    """

    label = "###### " + label.upper() + " ######"
    serialized_productions = [label.encode("utf8")] #put the comment on the first line
    for line in productions: #flatten list
        serialized_productions = serialized_productions + [line]

    fw = codecs.open(filename, "w", encoding="utf8")
    for line in serialized_productions:
        #[TODO] WRITE UNICODE VALUES AS UTF8 CHARACTERS TO FILE?
        print >> fw, line #each list item on new line
    fw.close()



def readFileAsStrippedList(filename, strip):
    """Read data from file in UTF8 as a list ready for processing

       Argument: filename (string) - file path to read from
                 strip (Bool) - switch for cleaning list
       Returns: lst (list)

    """
    f = codecs.open(filename, 'r', encoding="utf8") #get data from file in UTF8
    lst = f.read().splitlines() #build a list
    f.close()

    if strip == True: #perhaps clean up list
        lst = stripList(lst)

    return lst



def buildWordlist(properties, filename, prnt):
    """Read words from CSV file and build them as lexical items in dictionaries

        Arguments:
            properties (list) - keys for the dictionary of this word type
            filename (string) - path to CSV file
            prnt (Boolean) - switch to print the prepared dictionary before returning it
        Returns: wordlist (dictionary)
    """
    roots = readFileAsStrippedList(filename, True)
    wordlist = []

    for root in roots:
        info = root.replace(" ","").split(",") #the values
        word = dict(zip(properties, info)) #a dictionary for one word
        wordlist.append(word)

    if prnt == True:
        for word in wordlist:
            print word['base'] +  " = " + str(word)

    return wordlist



def generateNouns(lex, roots_file):
    """Generate noun forms

        Arguments: lex (list) - corresponding lexical productions entered by hand
                    roots_file - path to file containing roots

        Returns: concatenated lex + gen (original productions + newly generated forms)
    """
    print "Generating NOUN forms"

    generated = [] # list ready for generated productions
    properties = ["gender", "base", "poss", "pl", "pospl"] #the characterstics which the forms will be built from i.e. the keys

    words = buildWordlist(properties, roots_file, True)

    for word in words:

        falen = "nonSure" #set error flag
        #if word in plural has slender ending, it should lenite, this variable goes into the declension frame
        quality, last_vowel, last_vowel_index = checkFinalConsonant(word["pl"])
        if quality == 'slender': falen = "+FALEN" #Following Adjective Lenition...
        else: falen = "-FALEN"

        #genarate prepositional case forms based on gender to simplify frames below slightly
        if word["gender"] == 'masc': word["prep"] = word["base"]
        elif word["gender"] == 'fem': word["prep"] = slenderise(word["base"])

        if (not(lenitable(word["base"]))): #reduced 6-frame for unlenitables, LEN underspecified

            #determine CAGR type

            cagr = ["neu", "neu", "neu"] #masc.rad.sg, fem.poss.sg, rad+prep.pl
            if (word["gender"] == "masc" and startsWithVowel(word["base"])): cagr[0] = "v" #masc.rad.sg
            elif (word["gender"] == "fem" and startsWithVowel(word["base"])): cagr[1] = "v" #fem.poss.sg

            if startsWithVowel(word["pl"]): cagr[2] = "v" #pl.rad+prep

            #singular
            if word["gender"] == "masc":
                decl_sg = [
                        'N[CAGR=' + cagr[0] + ', CASE=rad, GEN=' + word["gender"] + '] -> "' + word["base"] + '"',
                        'N[CAGR=vflnr, CASE=prep, GEN=' + word["gender"] + '] -> "' + word["prep"] + '"',
                        'N[CAGR=vflnr, CASE=poss, GEN=' + word["gender"] + ']-> "' + word["poss"] + '"'
                        ]

            elif word["gender"] == "fem": #different CAGR
                decl_sg = [
                        'N[CAGR=vflnr, CASE=rad, GEN=' + word["gender"] + '] -> "' + word["base"] + '"',
                        'N[CAGR=vflnr, CASE=prep, GEN=' + word["gender"] + '] -> "' + word["prep"] + '"',
                        'N[CAGR=' + cagr[1] + ', CASE=poss, GEN=' + word["gender"] + ']-> "' + word["poss"] + '"'
                        ]

            #plural - just one pattern
            decl_pl = [
                    'N[CAGR=' + cagr[2] + ', CASE=rad, GEN=pl, ' + falen + ']-> "' + word["pl"] + '"',
                    'N[CAGR=' + cagr[2] + ', CASE=prep, GEN=pl, ' + falen + ']-> "' + word["pl"] + '"',
                    'N[CAGR=neu, CASE=poss, GEN=]-> "' + word["poss"] + '"' #no +FALEN because poss never slender in plural (ex. daoine)
                    ]

        else: #standard 12-frame, with explicit LEN

            cagr = ["neu", "neu", "neu"] #masc.rad.sg, (masc.prep+poss.sg|fem.rad+prep.sg), #poss.pl

            if (word["gender"] == "masc" and isLabial(word["base"][0])): cagr[0] = "lab" #masc.rad.sg, vowels caught in 6-frame

            #masc.prep+poss.sg, fem.rad+prep.sg
            elif ((word["base"][0]) == "s"): cagr[1] = "s"  #sp st sg caught in 6-frame

            #masc.prep+poss.sg, fem.rad+poss.sg
            elif ((word["base"][0]) == "f"): cagr[1] = "vflnr" #vlnr caught in 6-frame

            #fem.poss.sg Vs caught in 6-frame

            if isLabial(word["pl"][0]):
                cagr[2] = "lab" #poss.pl

            #singular
            if word["gender"] == "masc":
                decl_sg = [
                    'N[CAGR=' + cagr[0] + ', CASE=rad, GEN=masc, -LEN] -> "' + word["base"] + '"',
                    'N[CAGR=neu, CASE=rad, GEN=masc, +LEN] -> "' + lenite(word["base"]) + '"',
                    'N[CAGR=neu, CASE=prep, GEN=masc, -LEN] -> "' + word["prep"] + '"',
                    'N[CAGR=' + cagr[1] + ', CASE=prep, GEN=masc, +LEN] -> "' + lenite(word["prep"]) + '"',
                    'N[CAGR=neu, CASE=poss, GEN=masc, -LEN]-> "' + word["poss"] + '"',
                    'N[CAGR=' + cagr[1] + ', CASE=poss, GEN=masc, +LEN]-> "' + lenite(word["poss"]) + '"',
                    ]

            elif word["gender"] == "fem": #no poss[+LEN] for GEN=fem, different CAGR
                decl_sg = [
                    'N[CAGR=neu, CASE=rad, GEN=fem, -LEN] -> "' + word["base"] + '"',
                    'N[CAGR=' + cagr[1] + ', CASE=rad, GEN=fem, +LEN] -> "' + lenite(word["base"]) + '"',
                    'N[CAGR=neu, CASE=prep, GEN=fem, -LEN] -> "' + word["prep"] + '"',
                    'N[CAGR=' + cagr[1] + ', CASE=prep, GEN=fem, +LEN] -> "' + lenite(word["prep"]) + '"',
                    'N[CAGR=neu, CASE=poss, GEN=fem, -LEN]-> "' + word["poss"] + '"',
                    ]

            #plural - just one pattern
            decl_pl = [
                    'N[CAGR=neu, CASE=rad, GEN=pl, -LEN, ' + falen + '] -> "' + word["pl"] + '"',
                    'N[CAGR=neu, CASE=rad, GEN=pl, +LEN, ' + falen + '] -> "' + lenite(word["pl"]) + '"',
                    'N[CAGR=neu, CASE=prep, GEN=pl, -LEN, ' + falen + '] -> "' + word["pl"] + '"',
                    'N[CAGR=neu, CASE=prep, GEN=pl, +LEN, ' + falen + '] -> "' + lenite(word["pl"]) + '"',
                    'N[CAGR=' + cagr[2] + ', CASE=poss, GEN=pl, -LEN]-> "' + word["pospl"] + '"', #no +FALEN because poss never slender in plural (ex. daoine)
                    'N[CAGR=neu, CASE=poss, GEN=pl, +LEN]-> "' + lenite(word["pospl"]) + '"',
                    ]

        dh_forms = []
        if (startsWithVowel(word["base"]) or word["base"][0] == 'f'): #additional dh' items for VLs and Fs
            dh_forms = [
                    'N[CAGR=do, CASE=prep, GEN=' + word["gender"] + ', +LEN] -> "' + dh_lenite(word["prep"]) + '"',
                    'N[CAGR=do, CASE=prep, GEN=pl, +LEN] -> "' + dh_lenite(word["pl"]) + '"'
                    ]

        for production in (['\n'] + decl_sg + decl_pl + dh_forms):
            generated.append(production) #add individual productions to list

    return lex + generated



def generateVerbs(lex, roots_file):
    print "Generating VERB forms"

    generated = [] # list ready for generated productions
    properties = ["base", "vn", "subcat"] #the characterstics which the forms will be built from i.e. the keys

    words = buildWordlist(properties, roots_file, True)

    #determine CAGR type
    cagr = range(4)

    return lex + generated



def generateAdjectives(lex, roots_file):
    """Generate adjective forms from a list of basic lexical productions

        Returns: a larger list of more forms
    """
    print "Generating ADJECTIVE forms"

    generated = [] # list ready for generated productions
    properties = ["base", "syl"] #the characterstics which the forms will be built from i.e. the keys

    words = buildWordlist(properties, roots_file, True)

    for word in words:
        #forms not marked for case
        if (not(lenitable(word["base"])) or word["base"][0] == 'f'):
            not_cased = [
                            'ABASE[+PRED] -> "' + word["base"] + '"',
                            'ACOMP -> "' + lenite(addFinalVowel(slenderise(word["base"]))) + '"'
                        ]
        else:
            not_cased = [
                            'ABASE[+PRED, -LEN] -> "' + word["base"] + '"',
                            'ABASE[+PRED, +LEN] -> "' + lenite(word["base"]) + '"',
                            'ACOMP[-LEN] -> "' + addFinalVowel(slenderise(word["base"])) + '"',
                            'ACOMP[+LEN] -> "' + lenite(addFinalVowel(slenderise(word["base"]))) + '"'
                        ]

        #forms marked for case
        cased = [
                    'ABASE[CASE=rad, GEN=masc, -LEN] -> "' + word["base"] + '"',
                    'ABASE[CASE=rad, GEN=masc, +LEN] -> "' + lenite(word["base"]) + '"',
                    'ABASE[CASE=prep, GEN=masc, +LEN] -> "' + lenite(word["base"]) + '"',
                    'ABASE[CASE=poss, GEN=masc, +LEN] -> "' + lenite(slenderise(word["base"])) + '"',

                    'ABASE[CASE=rad, GEN=fem, +LEN] -> "' + lenite(word["base"]) + '"',
                    'ABASE[CASE=prep, GEN=fem, +LEN] -> "' + lenite(slenderise(word["base"])) + '"'
                ]

        #forms marked for case, with syllables playing a role
        if word["syl"] == 'mono':
            #monosyllabic
            cased_syl = [
                            'ABASE[CASE=poss, GEN=fem, -LEN] -> "' + lenite(addFinalVowel(slenderise(word["base"]))) + '"',
                            'ABASE[CASE=?cs, GEN=pl, -LEN] -> "' + addFinalVowel(slenderise(word["base"])) + '"',
                            'ABASE[CASE=?cs, GEN=pl, +LEN] -> "' + lenite(addFinalVowel(slenderise(word["base"]))) + '"',
                        ]
        else:
            #non-monosyllabic, hopefully multisyllabic
            cased_syl = [
                            'ABASE[CASE=poss, GEN=fem, -LEN] -> "' + lenite(slenderise(word["base"])) + '"',
                            'ABASE[CASE=?cs, GEN=pl, -LEN] -> "' + slenderise(word["base"]) + '"',
                            'ABASE[CASE=?cs, GEN=pl, +LEN] -> "' + lenite(slenderise(word["base"])) + '"',
                        ]


        for production in (['\n'] + not_cased + cased + cased_syl):
            generated.append(production) #add individual productions to list

    return lex + generated


def compileGrammar():
    """Read individual sections of the grammar, process them and concatenate them to main fcfg ready for the parser

        Arguments: none
        Returns: none

    """

    #get filenames and set up variables
    path_src = os.path.join(os.path.dirname(__file__), 'src/')
    path_gen = os.path.join(os.path.dirname(__file__), 'gen/')
    path_roots = os.path.join(os.path.dirname(__file__), 'roots/')

    files = os.listdir(path_src) #the files to start with are in the /src directory

    compiled_grammar = []

    #detect if files need any generation of lexical productions, and pass them to the appropriate functions if they do
    #here the detection is based on filenames, but it could also be done manually, or from the syntax with extra work
    for file in files:
        raw_data = readFileAsStrippedList(path_src + file, True) #read and strip comments

        gen = []
        #pass these to appropriate generating functinos
        if file =="adjectives_lex.fcfg":
            roots_file = path_roots + "adjectives.txt"
            gen = generateAdjectives(raw_data, roots_file)
        elif file=="nouns_lex.fcfg":
            roots_file = path_roots + "nouns.txt"
            gen = generateNouns(raw_data, roots_file)
        elif file=="verbs_lex.fcfg":
            roots_file = path_roots + "verbs.txt"
            gen = generateVerbs(raw_data, roots_file)
        else:
            print
            #TEMPORARILY SUSPENDED FOR DEVELOPMENT OF THE GENERATING FUNCTIONS
            #gen = raw_data

        #when they come back with extra lexical productions or not, save these intermediate versions in the /gen directory
        saveToFile(gen, file.rstrip(".fcfg"), path_gen + file)

    full_grammar = []
    #take data from generated files (gen) and serialize it into the main fcfg
    for file in files:
        raw_data = readFileAsStrippedList(path_gen + file, False) #read and keep comments
        for line in raw_data:
                full_grammar.append(line)

    saveToFile(full_grammar, " !!! FULL GRAMMAR", 'gaelic.fcfg')



def generateMultiwords():
    """Go through the full grammar and extract multiword tokens, and write them to the multiwords.txt file, ready for use in preprocessing

        Arguments: none
        Returns: none, writes to multiwords.txt file
    """
    fr = codecs.open('gaelic.fcfg' , 'r', encoding='utf8')
    grammar = fr.readlines()
    fr.close()

    grammar = stripList(grammar)
    multiwords = []

    multiword_token = re.compile(u"[\w\-']*_[\w\-']*", re.UNICODE) #[TODO] there's something wrong with the number of escapes and Rs and Us in this, but it seems to work
    for line in grammar:
        match = multiword_token.findall(line)
        if match:
            multiwords += match

    fw = codecs.open('multiwords.txt', 'w', encoding='utf8')
    for word in multiwords:
        #have the plain orthography (with spaces) ready for matching in plain orthography sentences
        word = word.replace('_', ' ')
        print>>fw, word #each list item on new line
    fw.close()



#[TODO] REFACTOR THE REWRITING RULES TO BE REVERSIBLE: THEY SHOULD TURN PUNCTUTATION AND CLITICS INTO SPACE-DELIMITED TOKENS, ABSTRACT THAT INTO A FUNCTION
def preprocessSentences(file_name):
    """Prepare contents of file for parsing

    Arguments:
    file_name - name of file with sentences to parse, one per line, comments allowed

    Returns:
    sentences - list of lowercased strings, with . and ? separated with spaces

    """
    f1 = open(file_name , 'r') #read in the default encoding, UTF8 does not work with grammars loaded using nltk.data.load()
    raw_sentences = f1.readlines()
    f1.close()

    sentences = []

    raw_sentences = stripList(raw_sentences) #remove comments, line breaks etc.

    #outputs sentences before preprocessing to check if the spaces match up
    #print 'before preprocessing: '
    #print raw_sentences

    for line in raw_sentences:
            #lowercase, delete line breaks, separate QMs and FSs with space so they get treated by the parser as words

            #[BUG] ON SOME PC PYTHON SHELLS THIS SHIFTS THE BYTES IN THE STRING AND MISMATCHES IN THE GRAMMAR, THE SOLUTION WOULD BE TO READ THE GRAMMAR IN IN UTF8, OR CHANGE THE ENCODING OF ALL THE FILES
            line = line.strip('\r\n').lower()

            #[TODO] NOT VERY PRETTY BUT QUICK, BEST DO THIS WITH REGEX
            #separate tokens with spaces
            for token in prespace_tokens:
                line = line.replace(token, " " + token)
            for token in postspace_tokens:
                line = line.replace(token, token + " ")

            #if no terminal symbol indicating S type, default to TS with full stop
            terminalSymbol = line[-1]
            if not(terminalSymbol == '.' or terminalSymbol == '?' or terminalSymbol == '!'):
                line = line + ' .'

            #link multiword tokens with underscores
            f2 = codecs.open('multiwords.txt' , 'r') #read in the default encoding, to match the encoding of the sentence file
            multiwords = f2.readlines()
            f2.close()
            for word in multiwords:
                word = word.rstrip('\n')
                if word in line:
                    wordUnderscored = word.replace(' ', '_')
                    line = line.replace(word, wordUnderscored)
            sentences.append(line)

    #this is the line which outputs preprocessed sentences to check if the spaces match up
    #print 'preprocessed: '
    #print sentences

    return sentences



def postprocessSentences(sentence):
    """Format string to conform to orthographic conventions

    Arguments:
    sentence - string as used by the parser

    Returns:
    sentence - capitalized string with punctuation
    """

    #capitalize, join FSs and QMs, strip underscores
    sentence = sentence.capitalize().replace('_', ' ')

    #[TODO] a very quick counterpart of the ugly code in the preprocessing function
    for token in prespace_tokens:
        sentence = sentence.replace(" " + token, token)
    for token in postspace_tokens:
        sentence = sentence.replace(token + " ", token)

    return sentence