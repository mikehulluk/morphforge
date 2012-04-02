#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import ply
import ply.lex
import ply.yacc
from morphforge.core.mgrs.locmgr import LocMgr
from tagselector import TagSelectorAll, TagSelectorAny
from tagselector import TagSelectorAnd, TagSelectorNot, TagSelectorOr

reserved = {
   'AND' : 'AND',
   'OR'  : 'OR',
   'NOT' : 'NOT',
   'ANY' : 'ANY',
   'ALL' : 'ALL',
}


tokens = [
    "LPARENS",
    "RPARENS",
    "LCURLYBRACKET",
    "RCURLYBRACKET",
    'COMMA',
    'TAG', 
    'AND_SYM',
    'OR_SYM',
    'NOT_SYM',
          ] + list( reserved.keys() )



t_AND_SYM =  r'&&'
t_OR_SYM  =  r'\|\|'
t_NOT_SYM =  r'!'
t_LPARENS =         r"""\("""
t_RPARENS =         r"""\)"""
t_LCURLYBRACKET =   r"""{"""
t_RCURLYBRACKET =   r"""}"""
t_COMMA =           r""","""
    
    
def t_TAG(t):
    r'[a-zA-Z_][a-zA-Z_0-9.]*'
    t.type = reserved.get(t.value,'TAG')
    return t


# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    assert False

t_ignore = " \t"


precedence = (
    ('left', 'OR', 'OR_SYM'),
    ('left', 'AND', 'AND_SYM'),
    ('right', 'NOT', 'NOT_SYM'),
)








def p_expression0(p):
    """ expr : tag_term_factor """  
    p[0] = p[1]


def p_expression1(p):
    """ expr : LPARENS expr RPARENS """  
    p[0] = p[2]


def p_expression_and(p):
    """ expr : expr AND expr
             | expr AND_SYM expr
    """  
    p[0] = TagSelectorAnd( p[1], p[3] ) 

def p_expression_or(p):
    """ expr : expr OR expr
             | expr OR_SYM expr
    """  
    p[0] = TagSelectorOr( p[1], p[3] )

def p_expression_not(p):
    """ expr : NOT expr
             | NOT_SYM expr
    """  
    p[0] = TagSelectorNot( p[2] )




def p_tag_term_factor(p):
    """tag_term_factor : tag_item_simple
                       | tag_group_factor_all
                       | tag_group_factor_any
                       """
    p[0] = p[1]
    
    

def p_tag_item_simple(p):
    """ tag_item_simple : TAG"""
    p[0] = TagSelectorAny( tags = [p[1]])


def p_tag_group_bracketed_all(p):
    """tag_group_factor_all : ALL tag_group_bracketed"""
    p[0] = TagSelectorAll( tags = p[2] )
    

def p_tag_group_bracketed_any(p):
    """tag_group_factor_any : ANY tag_group_bracketed"""
    p[0] = TagSelectorAny( tags = p[2] )



def p_tag_group_bracketed(p):
    """ tag_group_bracketed : LCURLYBRACKET tag_group RCURLYBRACKET """
    p[0] = p[2]
    
 
 
def p_tag_group0(p):
    """tag_group : empty"""
    p[0] = []

def p_tag_group1(p):
    """tag_group : TAG"""
    p[0] = [p[1]]
    
def p_tag_group2(p):    
    """tag_group : tag_group COMMA TAG"""
    p[0] = p[1] + [p[3]]



def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Syntax error in input!"
    print p
    assert False




def parseString( s):
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc(tabmodule='tagselectorparser_parsetab', outputdir=LocMgr.EnsureMakeDirs('/tmp/parsetabs/') )
    return parser.parse(s, lexer=lexer)


#
#
#tests = [
#    "ALL{}",
#    "ANY{spikes, hello}",
#    "hello",
#    "ALL{Current} AND ALL{Event}",
#    "ALL{Current} AND ALL{Event} AND NOT spike",
#    "ALL{Current} && (ALL{Event} ||  !spike AND ALL{hj,asd,eff,d})",
#    
#    ]
#
#
#
#class MockObjectTrace(object):
#    def __init__(self, tags):
#        self.tags = tags
#
#testTraces = [
#              MockObjectTrace( tags = ['spikes']),
#              MockObjectTrace( tags = ['hello']),
#              MockObjectTrace( tags = ['spikes', 'events'])
#              ]
#
#
#for t in tests:
#     p = parseString(t)
#     for tt in testTraces:
#         print tt.tags, p(tt) 
#     
#     print p
#
#
