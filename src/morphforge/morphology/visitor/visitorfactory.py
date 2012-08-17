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

import numpy as np
from morphforge.morphology.visitor.visitorbaseclasses import DictBuilderSectionVisitorHomo
from morphforge.morphology.visitor import SectionVisitorDF


class SectionVistorFactory(object):

    @classmethod
    def get_bounding_box(cls, morph=None):
        pts = SectionVistorFactory.array3_all_points(morph)()
        return (np.min(pts[:,0]), np.max(pts[:,0])) , (np.min(pts[:,1]), np.max(pts[:,1])), (np.min(pts[:,2]), np.max(pts[:,2]))


    @classmethod
    def array4_all_points(cls, morph=None):
        xyzr = []

        def functorRoot(s):
            xyzr.append(s.get_proximal_npa4())
            xyzr.append(s.get_distal_npa4())

        def functor(s):
            xyzr.append(s.get_distal_npa4())

        return SectionVisitorDF(functor=functor, morph=morph,
                                rootsectionfunctor=functorRoot,
                                returnfunctor=lambda : np.array(xyzr))

    @classmethod
    def array3_all_points(cls, morph=None):
        xyz = []

        def functorRoot(s):
            xyz.append(s.get_proximal_npa3())
            xyz.append(s.get_distal_npa3())

        def functor(s):
            xyz.append(s.get_distal_npa3())

        return SectionVisitorDF(functor=functor, morph=morph,
                                rootsectionfunctor=functorRoot,
                                returnfunctor=lambda : np.array(xyz))

    @classmethod
    def dict_section_proximal_dist_from_soma(cls, morph=None,
            soma_centre=False):
        assert not soma_centre

        def dict_section_proximal_dist_from_soma(s):
            if s.is_dummy_section():
                assert False

            if s.is_a_root_section():
                return 0.0
            else:
                d1 = dict_section_proximal_dist_from_soma(s.parent)
                d2 = s.parent.get_length()
                d = d1 + d2
                return d

        return DictBuilderSectionVisitorHomo(functor=dict_section_proximal_dist_from_soma, morph=morph)

    @classmethod
    def dict_section_distal_dist_from_soma(cls, morph=None):

        def dictSectionDistalDistFromSoma(s):
            if s.is_a_root_section():
                return s.get_length()
            else:
                return dictSectionDistalDistFromSoma(s.parent) + s.get_length()

        return DictBuilderSectionVisitorHomo(functor=dictSectionDistalDistFromSoma,
                morph=morph)


SVVisitorFactory = SectionVistorFactory

