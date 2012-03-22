# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GAELIC GRAMMAR WORD-LEVEL OPERATIONS
# Purpose:     Inflecting words using common Gaelic grammatical phenomena
#
# Author:      Wojtek Dziejma, supervised by Mark McConville
#
# Created:     2011-12
# Copyright:   (c) Wojtek Dziejma 2012
# Licence:     GPLv3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import re


#define a tuple of letter combinations which do not lenite
unlenited_initials = (u'l', u'n', u'r',  u'à', u'a', u'ì', u'i', u'e', u'è', u'o', u'ò', u'u', u'ù', u'sp', u'st', u'sg')

#NOT NEEDED BUT KEPT FOR REFERENCE
#define a tuple of byte patterns in UTF8 that correspond to initial long vowels in unicode
#unlenited_unicode_sigs = ('\xc0','\xe0', '\xd2','\xf2', '\xcc', '\xec', '\xc8','\xe8', '\xd9', '\xf9')

#collate entire list of unlenitables, account for capital letters and unicode
unlenited_initials = unlenited_initials + tuple([inital[0].upper() for inital in unlenited_initials])

broad_vowels = unicode('à|À|a|A|o|O|ò|Ò|u|U|ù|Ù', 'utf8')
slender_vowels = unicode('ì|Ì|i|I|e|E|è|È','utf8')
vowels = broad_vowels + "|" + slender_vowels

#[TODO] it might be very difficult to account for homorganic blocking...
#this would just take an unlenited token but would need a [+HOMORG] to fit in the productions... but how to detect these combinations in the parser?
#Rare, acknowledge in thesis and move on?



def lenitable(word):
    """Check if a word will change form when lenited

        Return      Boolean
    """
    if (word[1] == 'h' or word.startswith(unlenited_initials)): #if unlenitable or already lenited
        return False
    else:
        return True

def dh_lenite(word):
    """Lenite word with reduplication of do/de

        Returns:    word_dh_lenited (string) - a dh_lenited version, if word takes dh_lenition
                    word - otherwise
    """
    #could implement check to see if it is already lenited, for better error checking

    if (word[0] == 'f'):
        word = "dh'" + lenite(word)
    elif startsWithVowel(word):
        word = "dh'" + word

    return word


def lenite(word):
    """Lenite a word

        Returns:    word_lenited (string) - a lenited version
                    word (string) - if word is already lenited, or starts with an unlenitable sound

    """
    if not(word[1] == 'h' or word.startswith(unlenited_initials) == True ): #if unlenitable or already lenited
        word_lenited = word[0] + 'h' + word[1:]
        return word_lenited
    else:
        return word

#[TODO] has problems evaluating toilichte - returns i instead of e - that's the \w+ instead of \w* - important at all?
def checkFinalConsonant(word):
    """evaluates the quality of the final consonant

        Returns:    quality - string, 'broad' or 'slender'
                    last_vowel - string
                    last_vowel_index - int, position of last_vowel as a NEGATIVE index

    """
    #set up the return values and control flag for nested loop
    last_vowel = ''
    last_vowel_index = -1
    found = False
    quality = ""

    #NOT NEEDED, LEFT FOR REFERENCE
    #word = word.encode('ascii') #make sure the word is in utf8 so it matches the utf8 regex string

    word_reversed = word[::-1] #flip the word back to front

    initial_vowel_pattern = '\w+?(' + vowels +')' #build the pattern, starting with 1+ of word characters with a LAZY operator, DON'T be GREEDY

    """
        [del]
        print "\n"
        print vowels
        print type(vowels)
        print initial_vowel_pattern
        print type(vowels)
        print word_reversed
        print type(word_reversed)
    """

    substr_match = re.match(initial_vowel_pattern, word_reversed) #get substring from end of word to last vowel, in reverse

    last_vowel = substr_match.group(0)[-1] #get the last character in the match object string, this is the last vowel in the word
    last_vowel_index = -substr_match.end() #make it negative to be correct for the original, non-reversed word i.e. matching index from end

    if (last_vowel in slender_vowels):
        quality = 'slender'
    else:
        quality = 'broad'

    return quality, last_vowel, last_vowel_index

def slenderise(word):
    """Slenderise the word

        Arguments: str word
        Return: str word OR str word_lenited

    """
    quality, last_vowel, last_vowel_index = checkFinalConsonant(word) #pass word to the regex function to get properties of the ending


    print last_vowel_index
    #[TODO] NOT SURE ABOUT THIS FIX, àrd TRIGGERS THE ERROR
    try:
        pre_vowel = word[last_vowel_index-1]
    except IndexError:
        print "pre-final vowel error during slenderisation"
        pre_vowel = ""

    if (endsWithVowel(word) or quality == 'slender'):
        return word
    elif (quality == 'broad'):
        if last_vowel == 'a' and pre_vowel == 'e': #final "ea" -> "ei"
            word_slenderised = word[:last_vowel_index-1] + 'ei' + word[last_vowel_index+1:]
        else: #just insert "i"
            word_slenderised = word[:last_vowel_index+1] + 'i' + word[last_vowel_index+1:]
        return word_slenderised
    #else:
    #    raise SlenderizationError, "Something went wrong with slenderizing the word"

def addFinalVowel(word):
    """Concatenate an appropriate broad or slender final vowel to adjectives, and to nouns in the genitive

        Will work on both mono- and multisyllabic words. If word ends with a vowel already, return False.
    """

    quality, last_vowel, last_vowel_index = checkFinalConsonant(word)

    if endsWithVowel(word):
        print word + ": already ends in a vowel"
    elif quality == 'slender': #also used for adding slender vowels to genitve forms
        word = word + 'e'
    elif quality == 'broad':
        word = word + 'a'
    #else:
    #    raise addVowelError, "Something went wrong with adding the vowel"

    return word

#THESE COULD BE REWRITTEN AS isVowel() BUT I WANTED TO MAKE IT EXPLICIT AS IT IS USED IN DIFFERENT FUNCTIONS
#[TODO] PERHAPS REWRITE
def endsWithVowel(word):
    """
        Arguments:  word (string)
        Return:     Boolean
    """
    if word[-1] in vowels:
        return True
    else:
        return False

def startsWithVowel(word):
    """
        Arguments:  word (string)
        Return:     Boolean
    """
    if word[0] in vowels:
        return True
    else:
        return False

def isLabial(char):
    """
        Arguments:  word (string)
        Return:     Boolean
    """
    if char[0] in ['b', 'p', 'f', 'm']: #only check the first character of the passed string, should be a single character anyway, maybe raise exception?
        return True
    else:
        return False


