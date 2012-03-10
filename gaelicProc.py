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
import gaelicOps

prespace_tokens = ["!", ".", "?"] #these strings will be preprocessed to separate them as tokens with a space BEFORE them
postspace_tokens = ["n-", "h-", "t-"] #and these with a space AFTER them

def stripList(lst):
    """Remove comments, blank lines etc. from a list of productions read from a file

    """
    lst_stripped = []
    for item in lst:
        if not(item.startswith('#') or item.startswith('\r\n') or item.startswith('\n') or len(item) == 0): #the \r\n is for non-Win filesystems
            lst_stripped = lst_stripped + [item]
    return lst_stripped

def getGenerationSources(filepath):
    #get data from file
    f = codecs.open(filepath, 'r', encoding='utf8')
    raw_data = f.read().splitlines()
    f.close()

    #prepare element for zipping into a dictionary, assume only one section, without irregular/regular forms for processing
    productions = [[]]
    production_names = ['static']

    #find separation markers for production classes
    try:
        index_reg = raw_data.index('### REGULAR ###')
    except ValueError:
        index_reg = False

    try:
        index_irreg = raw_data.index('### IRREGULAR ###')
    except ValueError:
        index_irreg = False

    #Establish order of reg/irreg source productions, and prepare dictionary values

    if (index_reg and index_irreg): #there is a division into static items, and regular/irregular generations
        #redeclare variables for 3-part structure
        productions = [[],[],[]]
        production_names = ['static', 'irregular', 'regular']
        if index_irreg < index_reg: #irreg then reg
            productions[0] = stripList(raw_data[:index_irreg-1])
            productions[1] = stripList(raw_data[index_irreg+1:index_reg-1])
            productions[2] = stripList(raw_data[index_reg+1:])
        else: #reg then irreg
            productions[0] = stripList(raw_data[:index_reg-1])
            productions[2] = stripList(raw_data[index_reg+1:index_irreg-1])
            productions[1] = stripList(raw_data[index_irreg+1:])
    else:
        productions[0] = stripList(raw_data) #everything just goes into the static productions if not reg/irreg tags found

    #build the dictionary out of keys and values
    productions = dict(zip(production_names, productions))

    return productions

def saveGeneratedOutput(productions, file):
    """Serializes dictionary and writes it to file

        Arguments: productions (dictionary)
        Returns: none, writes to file
    """

    for value in productions.values():
        value = stripList(value)

    serialized_productions = [] #make sure the output file will be UTF-8 when read back into Python
    for section_name, section in productions.iteritems(): #loop through keys and values
        section_name = '### ' + section_name.upper() + ' ###' #prepare keys as comments
        serialized_productions = serialized_productions + [section_name] + section #remember to cast section_name as list so it can be concatenated with the list-type values items

    #write full clean output to file ready for parsing
    fw = codecs.open(file, 'w', encoding='utf8')
    for line in serialized_productions:
        print>>fw, line #each list item on new line
    fw.close()

#[TODO] THESE 3 FUNCTIONS WHEN GRAMMAR STRUCTURE IS SETTLED FINALLY
def buildNouns(productions):
    return False

def buildVerbs(productions):
    return False

def buildAdjectives(productions):
    """Generate adjective forms from a list of basic lexical productions

        Returns: a larger list of more forms
    """
    print "Processing adjectives..."
    #input pattern

    #[Q] does this pseudocode seem reasonable?
    #create a 'productions' dictionary with items {a_*}:{productions list}

    #detect the two different list elements: monosyllabic, multisyllabic (according to SYL variable) see regular_adjectives.fcfg - certainly move this to compileGrammar(), and pass mono as T/F, with the argument being a string
    #split the strings into an 'adjectives' list according to " | " - abstract this to a function later on
    #for adjective in adjectives:

    #if mono - addFinalVowel(adjective) in productions['a_gen_masc'], productions['a_gen_fem'], productions['a_all_pl']
    #concatenate lists into strings with the " | " separator - abstract this to a function later on
    #return the list


def compileGrammar():
    """Read individual sections of the grammar, process them and concatenate them to main fcfg ready for the parser

        Arguments: none
        Returns: none

    """

    #get filenames and set up variables
    path_src = os.path.join(os.path.dirname(__file__), 'src/')
    path_gen = os.path.join(os.path.dirname(__file__), 'gen/')

    files = os.listdir(path_src)

    grammar_sections = []
    compiled_grammar = []

    #read in contents of files into grammar_sections

    #prepare keys for dictionary from filenames
    grammar_section_names = [filename.rstrip('.fcfg') for filename in files]

    #take data from source files (src) generate forms and save individually as generated sections (gen)
    for file in files:
        temp = getGenerationSources(path_src + file)
        saveGeneratedOutput(temp, path_gen + file)

    #[TODO] INSERT PROCESSING FUNCTIONS
        #processX()
            #process static, irreg and reg according to rules
            #return lists

    #take data from generated files (gen) and serialize it into the main fcfg

    for file in files:
        f = codecs.open(path_gen + file, 'r', encoding='utf8')
        raw_data = f.read().splitlines()
        f.close()

        raw_data = stripList(raw_data)

        grammar_data = []
        for line in raw_data:
                grammar_data.append(line)
        #append stripped grammar to main 2D array
        grammar_sections.append(grammar_data)

    #build and save dictionary of sections
    grammar = dict(zip(grammar_section_names, grammar_sections))

    #[TODO] Python dictionaries cannot be sorted... think of a different structure for the data maybe? or live with the fact that it is unsorted in the file

    saveGeneratedOutput(grammar, 'gaelic.fcfg')

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

    #just here for a quick check in the interpreter
    #print 'Extracted multiwords: '
    #print multiwords


#[TODO] REFACTOR THE REWRITING RULES TO BE REVERSIBLE
#THEY SHOULD TURN PUNCTUTATION AND CLITICS INTO SPACE-DELIMITED TOKENS
#ABSTRACT THAT INTO A FUNCTION
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
#END preprocessSentences()

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