#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import re

ds = re.compile(r"""^ \s* (?P<quotes>\"{3}) (?P<ds>.*?) (?P=quotes) """, re.VERBOSE | re.MULTILINE| re.DOTALL)
m = ds.match( open('testHoook1.py').read() )

print m
print m.groupdict()['ds']



#import parser
#
#st = parser.suite( open('testHoook1.py').read() )
#tup = st.totuple()
#
#
#
#
#import symbol
#import token
#from types import ListType, TupleType
#
#def match(pattern, data, vars=None):
#    if vars is None:
#        vars = {}
#    if type(pattern) is ListType:
#        vars[pattern[0]] = data
#        return 1, vars
#    if type(pattern) is not TupleType:
#        return (pattern == data), vars
#    if len(data) != len(pattern):
#        return 0, vars
#    for pattern, data in map(None, pattern, data):
#        same, vars = match(pattern, data, vars)
#        if not same:
#            break
#    return same, vars
#DOCSTRING_STMT_PATTERN = (
#    symbol.stmt,
#    (symbol.simple_stmt,
#     (symbol.small_stmt,
#      (symbol.expr_stmt,
#       (symbol.testlist,
#        (symbol.test,
#         (symbol.and_test,
#          (symbol.not_test,
#           (symbol.comparison,
#            (symbol.expr,
#             (symbol.xor_expr,
#              (symbol.and_expr,
#               (symbol.shift_expr,
#                (symbol.arith_expr,
#                 (symbol.term,
#                  (symbol.factor,
#                   (symbol.power,
#                    (symbol.atom,
#                     (token.STRING, ['docstring'])
#                     )))))))))))))))),
#     (token.NEWLINE, '')
#     ))
#
#print tup[1]
#found, vars = match(DOCSTRING_STMT_PATTERN, tup[1])
#print found
#print vars
