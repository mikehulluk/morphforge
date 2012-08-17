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

from morphforge.morphology.core import MorphLocation

class CellLocation(object):

    def __init__(self, cell, morphlocation=None, section=None, sectionpos=None):
        self._cell = cell

        if morphlocation:
            assert not section and not sectionpos
            self.morphlocation = morphlocation
        else:
            assert not morphlocation
            self.morphlocation = MorphLocation(section=section,
                                               sectionpos=sectionpos)

        assert not self.morphlocation.section.is_dummy_section()

    def get_cell(self):
        return self._cell

    cell = property(get_cell, None, None)

    # We want to be able to treat CellLocations as locations,
    # so that we can measure between them for example:

    @property
    def section(self):
        return self.morphlocation.section

    @property
    def sectionpos(self):
        return self.morphlocation.sectionpos

    def get_3d_position(self):
        return self.morphlocation.get_3d_position()

    def get_location_description_str(self):
        r = self.cell.name
        t = ''
        if self.morphlocation.section.idtag:
            t = self.morphlocation.section.idtag
        return r + t

