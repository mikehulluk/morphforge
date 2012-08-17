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

from morphforge.morphology.core import MorphologyTree
from morphforge.morphology.exporter.morphologyexporter import MorphologyExporter

from Cheetah.Template import Template
from morphforge.core import FileIO
from morphforge.morphology.visitor import SectionIndexerWithOffsetDF
from morphforge.morphology.conversion.region_to_int_bimap import AutoRegionToIntMapTable

swc_templ = """
#---------------------------------
# SWC File Generated by morphforge
# --------------------------------

### Dummy Section:
#set dummy = $morph.get_dummy_section
$ids[dummy] 0 $dummy.d_x $dummy.d_y $dummy.d_z $dummy.d_r -1
#for $seg in $morph :
$ids[seg] $region_type_map[$seg] $seg.d_x $seg.d_y $seg.d_z $seg.d_r $ids[$seg.parent]
#end for

#---------------------------------
"""


class SWCTreeWriter(object):

    @classmethod
    def to_str(cls, morph=None, morphs=None, regionname_to_int_map=None):

        assert (morph or morphs) and not (morph and morphs)

        if morph:
            return cls._to_str_multi(morphs=[morph],
                    regionname_to_int_map=regionname_to_int_map)
        else:
            return cls._to_str_multi(morphs=morphs,
                    regionname_to_int_map=regionname_to_int_map)

    @classmethod
    def to_file(cls, filename, morph=None, morphs=None, regionname_to_int_map=None):
        assert (morph or morphs) and not(morph and morphs)

        if morph:
            return cls._to_file_multi(
                    morphs=[morph],
                    filename=filename,
                    regionname_to_int_map=regionname_to_int_map)
        else:
            return cls._to_file_multi(morphs=morphs, filename=filename,
                    regionname_to_int_map=regionname_to_int_map)

    @classmethod
    def _to_file_multi(cls, filename, morphs, regionname_to_int_map=None):
        return FileIO.write_to_file(txt=cls._to_str_multi(morphs, regionname_to_int_map=regionname_to_int_map) , filename=filename)

    @classmethod
    def _to_str_multi(cls, morphs, regionname_to_int_map=None):
        offset = 0
        output = ''
        for morph in morphs:
            offset = offset + 1

            # Add an additional section for the dummy section:
            dummy_offset = offset
            offset = offset + 1

            id_map = SectionIndexerWithOffsetDF(morph=morph, offset=offset)()
            id_map[morph.get_dummy_section()] = dummy_offset

            if regionname_to_int_map is None:
                regionname_to_int_map = AutoRegionToIntMapTable()

            region_type_map = dict((s, 0) if not s.region else (s,regionname_to_int_map.region_name_to_int(s.region.name)) for s in morph)

            context = [{'morph': morph, 'ids': id_map,
                       'region_type_map': region_type_map}]
            new_op = Template(swc_templ, context).respond()
            output += new_op
            offset += len(id_map)
        return output


MorphologyExporter.register("toSWCFile", lambda filename,morphology: SWCTreeWriter.to_file(filename=filename, morph=morphology), allow_override=False, from_type=MorphologyTree)
MorphologyExporter.register("toSWCStr",  lambda morphology: SWCTreeWriter.to_str(morph=morphology), allow_override=False, from_type=MorphologyTree)
