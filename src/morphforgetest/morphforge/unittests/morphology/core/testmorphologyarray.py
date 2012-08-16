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


from morphforge.morphology.core.array import MorphologyArray




class TestMorphologyArray(object):


    def testValidConstruction1(self):
        m = MorphologyArray(vertices= ([0,0,0,1],[0,0,1,1]) , connectivity = ([1,0],))
        assert len(m) == 1
        assert set( m.connections_to_index(0) ) == set([1])
        assert set( m.connections_to_index(1) ) == set([0])



        m = MorphologyArray(vertices= ([0,0,0,1],[0,0,1,1],[0,0,2,1]) , connectivity = ([1,0],[1,2]))
        assert set( m.connections_to_index(0) ) == set([1])
        assert set( m.connections_to_index(1) ) == set([0,2])
        assert set( m.connections_to_index(2) ) == set([1])
        assert len(m) == 2

        m = MorphologyArray(vertices= ([0,0,0,1],[0,0,1,1],[0,0,2,1]) , connectivity = ([1,0],[2,0]))
        assert set( m.connections_to_index(0) ) == set([1,2])
        assert set( m.connections_to_index(1) ) == set([0])
        assert set( m.connections_to_index(2) ) == set([0])
        assert len(m) == 2


    def testConstruction2(self):
        pass

    def testConstruction3(self):
        pass
    def testConstruction4(self):
        pass



if __name__ == "__main__":
    TestMorphologyArray().testValidConstruction1()



