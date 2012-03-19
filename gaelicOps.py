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

unlenited_initials = ('l', 'n', 'r',  'à', 'a', 'ì', 'i', 'e', 'è', 'o', 'ò', 'u', 'ù', 'sp', 'st', 'sg') #define a tuple of letter combinations which do not lenite
unlenited_initials = unlenited_initials + tuple([inital[0].upper() for inital in unlenited_initials]) #account for capital letters

broad_vowels = unicode('à|À|a|A|o|O|ò|Ò|u|U|ù|Ù', 'utf8')
slender_vowels = unicode('ì|Ì|i|I|e|E|è|È','utf8')
vowels = broad_vowels + "|" + slender_vowels

#[TODO] it might be very difficult to account for homorganic blocking...
#this would just take an unlenited token but would need a [+HOMORG] to fit in the productions... but how to detect these combinations in the parser?
#Rare, acknowledge in thesis and move on?

def lenite(word):
    """Lenite a word

    If word is already lenited, or starts with an unlenitable sound, return False

    """
    if not(word[1] == 'h' or word.startswith(unlenited_initials) == True ): #if unlenitable or already lenited
        word_lenited = word[0] + 'h' + word[1:]
        return word_lenited
    else:
        return word

#[Q] has problems evaluating toilichte - returns i instead of e - that's the \w+ instead of \w* - important at all?
def checkFinalConsonant(word):
    """evaluates the quality of the final consonant

        Arguments:
            word - string
        Returns:
            quality - string, 'broad' or 'slender'
            last_vowel - string
            last_vowel_index - int, position of last_vowel as a NEGATIVE index

    """
    #set up the return values and control flag for nested loop
    last_vowel = ''
    last_vowel_index = -1
    found = False

    word = word.decode('utf8') #make sure the word is in utf8 so it matches the utf8 regex string
    word_reversed = word[::-1] #flip the word back to front

    initial_vowel_pattern = '\w+?(' + vowels +')' #build the pattern, starting with 1+ of word characters with a LAZY operator, DON'T be GREEDY

    substr_match = re.match(initial_vowel_pattern, word_reversed) #get substring from end of word to last vowel, in reverse

    last_vowel = substr_match.group(0)[-1] #get the last character in the match object string, this is the last vowel in the word
    last_vowel_index = -substr_match.end() #make it negative to be correct for the original, non-reversed word i.e. matching index from end

    if (last_vowel in slender_vowels):
        quality = 'slender'
    else:
        quality = 'broad'

    return quality, last_vowel, last_vowel_index

def slenderize(word):
    """Slenderize the word

        Arguments: str word
        Return: str word OR str word_lenited

    """
    quality, last_vowel, last_vowel_index = checkFinalConsonant(word) #pass word to the regex function to get properties of the ending

    pre_vowel = word[last_vowel_index-1]

    if (hasFinalVowel(word) or quality == 'slender'):
        return word
    elif (quality == 'broad'):
        if last_vowel == 'a' and pre_vowel == 'e':
            word_slenderized = word[:last_vowel_index-1] + 'ei' + word[last_vowel_index+1:]
        else:
            word_slenderized = word[:last_vowel_index+1] + 'i' + word[last_vowel_index+1:]
        return word_slenderized
    else:
        raise SlenderizationError, "Something went wrong with slenderizing the word"

def addFinalVowel(word):
    """Concatenate an appropriate broad or slender final vowel to adjectives, and to nouns in the genitive

        Will work on both mono- and multisyllabic words. If word ends with a vowel already, return False.
    """

    if hasFinalVowel(word):
        print "already end is a vowel"
    elif quality == 'slender': #also used for adding slender vowels to genitve forms
        word = word + 'e'
    elif quality == 'broad':
        word = word + 'a'
    else:
        raise addVowelError, "Something went wrong with adding the vowel"

    return word

def hasFinalVowel(word):
    """Test to see if word ends in a vowel

        Arguments: str word
        Return: Boolean
    """
    if word[-1] in vowels:
        return True
    else:
        return False