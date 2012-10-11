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

import ply
import ply.lex
import ply.yacc

from morphforge.core import LocMgr, SettingsMgr
from morphforge.traces.tracetypes.tracepiecewise import TracePiecewise

# Lexing:
from morphforge.traces.generation.gen_parser_lexer import TraceGeneratorParserLexer
l = TraceGeneratorParserLexer()
tokens = l.tokens



# pylint: disable=W0611
# Parsing
from morphforge.traces.generation.gen_parser_yacc import p_complete
from morphforge.traces.generation.gen_parser_yacc import p_unit_definiton
from morphforge.traces.generation.gen_parser_yacc import p_time
from morphforge.traces.generation.gen_parser_yacc import p_abs_timespec
from morphforge.traces.generation.gen_parser_yacc import p_end_timespec
from morphforge.traces.generation.gen_parser_yacc import p_func
from morphforge.traces.generation.gen_parser_yacc import p_func_name
from morphforge.traces.generation.gen_parser_yacc import p_pieceblock_chain1
from morphforge.traces.generation.gen_parser_yacc import p_pieceblock_chain2
from morphforge.traces.generation.gen_parser_yacc import p_pieceblock_chain3
from morphforge.traces.generation.gen_parser_yacc import p_pieceblock_chain4
from morphforge.traces.generation.gen_parser_yacc import p_pieceblock_chain_complete
from morphforge.traces.generation.gen_parser_yacc import p_error


class TraceStringParser(object):

    @classmethod
    def Parse(cls, s):
        return cls._trace_from_string(s)

    @classmethod
    def _trace_from_string(cls, srcstr):
        parser = ply.yacc.yacc(tabmodule='tracestring_parsetab',
                                outputdir=LocMgr.ensure_dir_exists('/tmp/parsetabs/'),
                                debug=SettingsMgr.get_ply_yacc_debug_flag())

        (unit, trace_prototypes) = parser.parse(srcstr, lexer=l)

        # Copy accross the start values:
        start_value = 0
        for prototype in trace_prototypes:
            prototype.start_value = start_value
            piece = prototype.toTracePiece()
            start_value = piece.get_end_value()

        # Convert to pieces
        pieces = [trace_prototype.toTracePiece() for trace_prototype in trace_prototypes]
        trace = TracePiecewise(pieces=pieces, comment='Src: %s' % srcstr)
        trace = trace * (1.0 * unit)
        return trace




#tests = [
#"""{d:pA} AT 0ms FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 120ms THEN FLAT(50) FOR 20ms """,
#"""{d:pA} AT 0ms FLAT(0) UNTIL 150ms THEN FLAT(120) FOR 20ms THEN FLAT(0) FOR 20ms""",
#"""{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 160ms""",
#"""{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 130ms THEN FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms""",
#"""{d:pA} FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms""",
# ]
#
#
#for t in tests:
#    tr = TraceStringParser.Parse(t)
#    #tr = trace_from_string(t)
#    tr.tags = ['Current']
#    TagViewer(tr)
#
