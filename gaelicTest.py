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

words = ["toilichte", "spòrsail", "cudromach", "beag", "àrd"]

def testThis():
    for word in words:
        word = gaelicOps.lenite(word)
        word = gaelicOps.slenderize(word)