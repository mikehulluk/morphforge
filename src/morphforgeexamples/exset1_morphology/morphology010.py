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


"""Creating morphologies from python dictionaries.
In this example, we create 2 :py:class:`MorphologyTree` objects from python
dictionaries, and then demonstrate iterating over the sections"""

from morphforge.morphology import MorphologyTree


# Build a morphology consisting of a single-section:
morphDict1 = {'root': {'length': 20, 'diam': 20} }
m1 = MorphologyTree.fromDictionary(morphDict1, name="SimpleMorphology1")
print "M1:"
for section in m1:
    print section


# Build a morphology consisting of a 2 compartments:
morphDict2 = {'root': {'length': 20, 'diam': 20, 'sections': [{'length': 300, 'diam': 2}]  } }
m2 = MorphologyTree.fromDictionary(morphDict2, name="SimpleMorphology2")
print "M2:"
for section in m2:
    print "Section:"
    print " - Proximal:",section.p_x,section.p_y, section.p_z, section.p_r
    print " - Distal:  ",section.d_x,section.d_y, section.d_z, section.d_r

