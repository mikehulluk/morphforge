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

import re
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionLinear
from morphforge.traces.tracetypes.tracepiecewise import TracePiecewise
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat
from morphforge.core.quantities.fromcore import unit
import quantities as pq
import itertools


class LevelToken(object):

    def __init__(self, symbol):
        self.symbol = symbol

    def does_consume(self):
        return False

    def record_time_in_symbol(self):
        return self.symbol

    def does_match(self, level):
        return True


class LevelSelector(object):

    def __init__(self, time_selector, data_selector):
        self.time_selector = time_selector
        self.data_selector = data_selector

    def does_match(self, level):
        return self.time_selector.does_match(level) \
            and self.data_selector.does_match(level)

    def does_consume(self):
        return True

    def record_time_in_symbol(self):
        return None


class DataSelector(object):

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def does_match(self, level):
        l_bound_ok = (self.minvalue < level.get_value() if self.minvalue is not None else True)
        u_bound_ok = (self.maxvalue > level.get_value() if self.maxvalue is not None else True)
        return l_bound_ok and u_bound_ok
class TimeSelector(object):
    def __init__(self, minduration=None, maxduration=None):
        self.minduration = minduration
        self.maxduration = maxduration
    def does_match(self, level):
        l_bound_ok = (self.minduration < level.get_duration() if self.minduration is not None else True)
        u_bound_ok = (self.maxduration > level.get_duration() if self.maxduration is not None else True)
        return l_bound_ok and u_bound_ok


class MatchObject(object):
    def __init__(self):
        self.d = {}
    def set_symbol(self, symbol, value):
        self.d[symbol] = value
    def __getattr__(self, name):
        if name in self.d:
            return self.d[name]

    def __str__(self,):
        return "<MatchObject: "+ ",".join(["%s=%s"%(k,v) for (k,v) in sorted(self.d.iteritems())]) + ">"



class LevelSelectorGroup(object):

    def __init__(self, S, xunit, yunit):
        # Parse the expression:
        self.expr = LevelSelectorGroup.parse_expr(S, xunit, yunit)
        self.xunit = xunit

    def matchall(self, level_set):
        pieces = level_set.pieces

        # From [A,B,C,D,..]
        # return [[A,B,C,D],[B,C,D],[C,D],[D]...]
        subgroups = []
        for i in range(len(pieces)):
            subgroups.append(pieces[i:])

        matches = [self.test_match(sg) for sg in subgroups]
        return [m for m in matches if m is not None]

    def test_match(self, level_pieces):

        # Check the lengths, so I don't need to worry about it later:
        if len(level_pieces) < len([t for t in self.expr
                                   if t.does_consume()]):
            return None

        m = MatchObject()
        level_piece_iter = itertools.chain(iter(level_pieces), [None])
        level_piece_next = level_piece_iter.next()

        current_time = level_piece_next.get_min_time()
        for t in self.expr:

            # Do we need to record the current time?
            rec = t.record_time_in_symbol()
            if rec:
                m.set_symbol(rec, current_time.rescale(self.xunit))

            # Does match?
            if not t.does_match(level_piece_next):
                return None

            # Next term:
            if t.does_consume():
                level_piece_next = level_piece_iter.next()
                if level_piece_next == None:
                    current_time = level_pieces[-1].get_max_time()
                else:
                    current_time = level_piece_next.get_min_time()

        return m

    @classmethod
    def parse_expr(cls, s, xunit, yunit):
        s = s.replace(' ', '')
        return [LevelSelectorGroup.parse_term(t, xunit, yunit) for t in
                s.split(',')]

    @classmethod
    def parse_term(cls, st, xunit, yunit):
        r_marker = re.compile(r"""(?P<name>[a-zA-Z0-9]+)""", re.VERBOSE)
        t_marker = \
            re.compile(r"""{ (?P<t0>[-]?\d+)? : (?P<t1>[-]?\d+)? @  (?P<d0>[-]?\d+)? : (?P<d1>[-]?\d+)? }"""
                       , re.VERBOSE)
        r_m = r_marker.match(st)
        if r_m:
            marker = r_m.groupdict()['name']
            return LevelToken(symbol=marker)

        t_m = t_marker.match(st)
        if not t_m:
            assert False, "Can't parse: %s" % st

        g = t_m.groupdict()
        (t0, t1, d0, d1) = (g['t0'], g['t1'], g['d0'], g['d1'])
        t0 = (int(t0) * xunit if t0 else None)
        t1 = (int(t1) * xunit if t1 else None)
        d0 = (int(d0) * yunit if d0 else None)
        d1 = (int(d1) * yunit if d1 else None)
        return LevelSelector(data_selector=DataSelector(d0, d1),
                             time_selector=TimeSelector(t0, t1))



l1 = TracePiecewise(pieces = [
                                TracePieceFunctionFlat(time_window=(0,50)*pq.ms, x=unit("0:pA")),
                                TracePieceFunctionFlat(time_window=(50,150)*pq.ms, x=unit("110:pA")),
                                TracePieceFunctionFlat(time_window=(150,350)*pq.ms, x=unit("0:pA")),
                                   ])



sel1 = LevelSelectorGroup(" A, { 10:65 @ -1:1 }, B, { 10: @ 90:111 }, C", xunit=unit("ms"), yunit=unit("pA"))

matches = sel1.matchall(l1)
for m in matches:
    print m

