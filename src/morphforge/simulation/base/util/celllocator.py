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

import itertools

from morphforge.morphology.util.morphlocator import MorphLocator
from morphforge.simulation.base.core.celllocation import CellLocation
from morphforge.core.misc import SeqUtils


class CellLocator(object):

    """Provides the same functionality as MorphLocator, except that it operates on cells."""

    @classmethod
    def get_locations_at_distance_away_from_dummy(cls, cell, distance, section_predicate=None):

        morphology_locations = MorphLocator.get_locations_at_distance_away_from_dummy(
                                        morphology=cell.morphology,
                                        distance=distance,
                                        section_predicate=section_predicate)
        return [CellLocation(cell=cell, morphlocation=morphology_location) for morphology_location in morphology_locations]


    @classmethod
    def get_locations_at_distances_away_from_dummy(cls, cell, distances, section_predicate=None):
        return list(itertools.chain(*[cls.get_locations_at_distance_away_from_dummy(cell=cell, distance=distance, section_predicate=section_predicate) for distance in distances] ))

    @classmethod
    def get_location_at_distance_away_from_dummy(cls, cell, distance, section_predicate=None):
        """Utility Function"""
        return SeqUtils.expect_single(cls.get_locations_at_distance_away_from_dummy(cell=cell, distance=distance, section_predicate=section_predicate))
