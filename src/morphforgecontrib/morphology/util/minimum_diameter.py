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


from morphforge.morphology.core import Section
from morphforge.morphology.core import Region
from morphforge.morphology.core import MorphologyTree




class MorphologyMinimumDiameter(object):


    @classmethod
    def ensure(cls, morphology, min_diameter):
        min_radius = min_diameter / 2.0

        section_mapping_table = {}
        region_mapping_table = {}

        # Create New Regions:
        region_mapping_table[None] = None
        for rOld in morphology.get_regions():
            r_new = Region(name=rOld.name)
            region_mapping_table[rOld] = r_new


        # Create New Sections:
        dummy_root_old = morphology.get_dummy_section()
        dummy_root_new = Section(
                    region=region_mapping_table[dummy_root_old.region],
                    x=dummy_root_old.d_x,
                    y=dummy_root_old.d_y,
                    z=dummy_root_old.d_z,
                    r=max(dummy_root_old.d_r,
                    min_radius))
        section_mapping_table[dummy_root_old] = dummy_root_new
        for sectionOld in morphology:

            old_parent = sectionOld.parent
            new_parent = section_mapping_table[old_parent]

            section_new = new_parent.create_distal_section(
                region=region_mapping_table[sectionOld.region],
                x=sectionOld.d_x,
                y=sectionOld.d_y,
                z=sectionOld.d_z,
                r=max(sectionOld.d_r, min_radius),
                idtag=sectionOld.idtag,
               )
            section_mapping_table[sectionOld] = section_new

        m = MorphologyTree(name=None, dummysection=dummy_root_new,
                           metadata={})

        assert len(m) == len(morphology)




        return m








