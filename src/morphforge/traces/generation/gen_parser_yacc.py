#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------


import quantities as pq

from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionLinear

from morphforge.core.quantities import unit






# Lexing:
from gen_parser_lexer import TraceGeneratorParserLexer
l = TraceGeneratorParserLexer()
tokens = l.tokens




class FunctionPrototype(object):
    def __init__(self, funcname, funcarg, start_time=None, end_time=None):
        self.funcname = funcname
        self.funcarg = funcarg
        self.start_time = start_time
        self.end_time = end_time

        self.start_value = None


    def toTracePiece(self):

        builddict = {
        'FLAT':   lambda window,arg, start_value:
                    TracePieceFunctionFlat(time_window=window, x=arg),
        'RAMPTO': lambda window, arg, start_value:
                    TracePieceFunctionLinear(time_window=window, x0=start_value, x1=arg),
        }

        p = builddict[self.funcname]( window=(self.start_time,self.end_time), arg=self.funcarg, start_value=self.start_value)
        return p








def p_complete(p):
    """ l : unit_def p_pieceblock_chain_complete"""
    p[0] =  p[1],p[2]



# Parsing:

def p_unit_definiton(p):
    """ unit_def : CURLY_LBRACE D COLON ID CURLY_RBRACE """
    p[0] = unit(p[4])

def p_time(p):
    """time : FLOAT MS"""
    p[0] = p[1] * pq.ms

def p_abs_timespec(p):
    """ abs_timespec : AT time """
    p[0] = p[2]


def p_end_timespec(p):
    """ end_timespec : UNTIL time
                     | FOR time
                     """
    p[0] = (p[1], p[2])

def p_func(p):
    ''' func : func_name LPAREN FLOAT RPAREN'''

    p[0] = FunctionPrototype(funcname=p[1], funcarg=p[3])

def p_func_name(p):
    """ func_name : FLAT
                  | RAMPTO"""
    p[0] = p[1]





def p_pieceblock_chain1(p):
    """pieceblock_chain : abs_timespec func """
    f = p[2]
    f.start_time = p[1]
    p[0] = ([], f)

def p_pieceblock_chain2(p):
    """pieceblock_chain : func """
    f = p[1]
    f.start_time = 0 * pq.ms
    p[0] = ([], f)

def p_pieceblock_chain3(p):
    """pieceblock_chain : pieceblock_chain THEN abs_timespec func"""
    t = p[3]
    (chain, last) = p[1]
    last.end_time = t
    f = p[4]
    f.start_time = t
    p[0] = (chain + [last], f)

def p_pieceblock_chain4(p):
    """pieceblock_chain : pieceblock_chain end_timespec THEN func"""
    (chain, last) = p[1]
    (ttype, tvalue) = p[2]
    t = {'UNTIL': tvalue, 'FOR': last.start_time + tvalue}[ttype]
    last.end_time = t
    f = p[4]
    f.start_time = t
    p[0] = (chain + [last], f)



def p_pieceblock_chain_complete(p):
    """p_pieceblock_chain_complete : pieceblock_chain  end_timespec"""
    (chain, last) = p[1]
    (ttype, tvalue) = p[2]
    t = {'UNTIL': tvalue, 'FOR': last.start_time + tvalue}[ttype]
    last.end_time = t
    p[0] = chain + [last]

# Error rule for syntax errors
def p_error(p):
    print 'Syntax error in input!', p
    assert False





