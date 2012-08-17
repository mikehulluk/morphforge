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
import quantities as pq


def parse(s):

    on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
    if on_rtd:
        print ' WARNING!! Read the Docs Hack - Not parsing unit:', s
        return 0 * pq.dimensionless

    # Upgraded on 9th Jun 2012 to use neurounits.
    # print "Parsing Unit:", s
    if s == 'ohmcm':
        s = 'ohm cm'

    # To resolve....
    if s == 'nMol':
        s = 'nanomolar'
    if s == 'uMol':
        s = 'micromolar'

    # In the case of units, lets rewrite '**' to nothing and '*' to space:
    s = s.replace('**', '')
    s = s.replace('*', ' ')

    if s.strip() == '':
        return pq.dimensionless
    import neurounits
    return neurounits.NeuroUnitParser.Unit(s).as_quantities_unit()







