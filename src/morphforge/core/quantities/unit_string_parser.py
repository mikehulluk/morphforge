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
#import ply.yacc as yacc
#
#from unit_string_lexer import tokens
#from unit_string_lexer import lexer
#
#import numpy as np
#
#
import quantities as pq
#
#from morphforge.core import LocMgr
#from morphforge.core import SettingsMgr
#
#def unit_from_string(unit_str):
#    return pq.unit_registry[unit_str]
#
#def p_empty(p):
#    'unit_str :'
#    p[0] = pq.dimensionless
#
#
#def p_unit_str_num_and_denom(p):
#    'unit_str : unit_expr DIVIDE unit_expr'
#    p[0] = p[1] / p[3]
#
#def p_unit_str_nom(p):
#    'unit_str : unit_expr'
#    p[0] = p[1]
#
#def p_unit_str_denom(p):
#    'unit_str : DIVIDE unit_expr'
#    p[0] = 1.0 / p[2]
#
#
#def p_unit_str_exprApp(p):
#    'unit_expr : unit_expr unit '
#    p[0] = p[1] * p[2]
#
#def p_unit_str_exprBase(p):
#    'unit_expr : unit '
#    p[0] = p[1]
#
#def p_unit_simple(p):
#    'unit : ID'
#    p[0] = unit_from_string( p[1] )
#
#
#def p_unit_simplenumber(p):
#    'unit : ID NUMBER'
#    u = unit_from_string( p[1] )
#    p[0] = np.power(u, p[2] )
#
#
#def p_error(p):
#    print "Syntax error in input!"
#    assert False
#
#
#
#parser = yacc.yacc(tabmodule = 'unitsparser_parsetab.py', outputdir=LocMgr.get_ply_parsetab_path('unitsparser'), debug=SettingsMgr.get_ply_yacc_debug_flag()  )
#

def parse(s):

    # Upgraded on 9th Jun 2012 to use neurounits.
    print "Parsing Unit:", s
    if s == 'ohmcm':
        s = 'ohm cm'

    # To resolve....
    if s== 'nMol':
        s = 'nanomolar'
    if s== 'uMol':
        s = 'micromolar'

    # In the case of units, lets rewrite '**' to nothing and '*' to space:
    s = s.replace("**", "")
    s = s.replace("*", " ")


    if s.strip() == "":
        return pq.dimensionless
    print s
    import neurounits
    return neurounits.NeuroUnitParser.Unit(s).as_quantities_unit() #, backend=neurounits.units_backends.)

    #r = parser.parse(s, lexer=lexer, )
    #return r






