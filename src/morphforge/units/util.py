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


import os

import morphforge
from morphforge.core.misc import is_float

import quantities as pq


def factorise_units_from_list(seq):
    assert len(seq) > 0

    for obj in seq:
        assert isinstance(obj, pq.quantity.Quantity)

    s0unit = seq[0].units
    new_list = [obj.rescale(s0unit).magnitude for obj in seq] * s0unit
    return new_list



def parse_unit_str(s):
    # TODO: HACK TO MAKE CERTAIN UNITS LOOK NICE
    if s == 'nA':
        return pq.nano * pq.amp
    if s == 'pA':
        return pq.pico * pq.amp
    if s == 'nS':
        return pq.nano * pq.S
    if s == 'pS':
        return pq.pico * pq.S
    if s == 'mV':
        return pq.mV

    # In the case of units, lets rewrite '**' to nothing and '*' to space:
    s = s.replace('**', '')
    s = s.replace('*', ' ')

    import neurounits
    return neurounits.NeuroUnitParser.Unit(s).as_quantities_unit()







# Lets cache the units:
_cached_units = {}
def qty(s):
    if not s in _cached_units:
        _cached_units[s] = _qty(s)
    return _cached_units[s]



def _qty(s):
    if isinstance(s, pq.quantity.Quantity):
        return s

    if is_float(s):
        return float(s) * pq.dimensionless


    if ':' in s:
        (value_str, unit_str) = s.split(':')
        value = float(value_str)
        unt = parse_unit(unit_str)
        return value * unt

    print s
    assert False, "MH I Don't think we get here, Oct 2012"

    if ' ' in s:
        print s
        assert False, "MH I Don't think we get here, Oct 2012"
        tokens = s.split(' ')
        if len(tokens) == 2:
            (value_str, unit_str) = tokens
            value = float(value_str)
            unt = parse_unit(unit_str)
            return value * unt
        else:
            assert False
    assert False, "MH I Don't think we get here, Oct 2012"
    return parse_unit(s)








def parse_unit(s):


    on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
    if on_rtd:
        print ' WARNING!! Read the Docs Hack - Not parsing unit:', s
        return 0 * pq.dimensionless

    s = s.strip()

    # Return nothing as no unit
    if s == '':
        return pq.dimensionless

    # TODO: HACK TO MAKE CERTAIN UNITS LOOK NICE
    if s == 'nA':
        return pq.nano * pq.amp
    if s == 'pA':
        return pq.pico * pq.amp
    if s == 'nS':
        return pq.nano * pq.S
    if s == 'pS':
        return pq.pico * pq.S
    if s == 'mV':
        return pq.mV


    ## Upgraded on 9th Jun 2012 to use neurounits.
    #if s == 'ohmcm':
    #    s = 'ohm cm'


    # In the case of units, lets rewrite '**' to nothing and '*' to space:
    s = s.replace('**', '')
    s = s.replace('*', ' ')

    import neurounits
    return neurounits.NeuroUnitParser.Unit(s).as_quantities_unit()

