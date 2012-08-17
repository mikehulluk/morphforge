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

from morphforge.morphology.visitor.visitorbaseclasses import SectionVisitorDF


class SectionVisitorDFNeuronBuilder(SectionVisitorDF):

    def __init__(self, transfunctor, morph=None):

        self.transfuctor = transfunctor

        self.orig2newMapping = None
        self.rgnMappings = None
        self.newMorph = None

        super(SectionVisitorDFNeuronBuilder,
              self).__init__(morph=morph, functor=self.build_extrusion,
                             dummysectionfunctor=self.build_root,
                             returnfunctor=lambda : self.newMorph)

        if self.morph != None:
            self.__call__()

    def build_root(self, section):
        from morphforge.morphology.core import Section, Region, MorphologyTree

        self.orig2newMapping = {}
        self.rgnMappings = dict([(rgn,Region(rgn.name)) for rgn in self.morph.get_regions()])
        self.newMorph = None

        (x, y, z, r) = (section.d_x, section.d_y, section.d_z, section.d_r)
        (X, Y, Z, R) = self.transfuctor(x, y, z, r)

        new_section = Section(regions=[self.rgnMappings[r] for r in section.regions], x=X, y=Y, z=Z, r=R)

        self.newMorph = MorphologyTree('MorphCloned', dummysection=new_section, metadata={})

        self.orig2newMapping[section] = new_section

    def build_extrusion(self, section):

        new_parent = self.orig2newMapping[section.parent]

        (x, y, z, r) = (section.d_x, section.d_y, section.d_z, section.d_r)
        (X, Y, Z, R) = self.transfuctor(x, y, z, r)

        new_section = new_parent.create_distal_section(regions=[self.rgnMappings[r] for r in section.regions], x=X, y=Y, z=Z, r=R)
        self.orig2newMapping[section] = new_section


