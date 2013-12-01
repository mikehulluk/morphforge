#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# -------------------------------------------------------------------------------

import numpy as np
import itertools

from morphforge.morphology.visitor.visitorfactory import SectionVistorFactory
from morphforge.morphology.core import MorphLocation
from morphforge.morphology.core import MorphPath


class MorphLocator(object):

    @classmethod
    def get_locations_at_distance_away_from_dummy(cls, morphology,
            distance, section_predicate=None):

        dist_to_section_distal = SectionVistorFactory.dict_section_distal_dist_from_soma(morph=morphology)()


        # Section predicates: allows us to generate only on a path, region, etc
        section_predicate = section_predicate if section_predicate else lambda s:True

        locations = []

        for section in morphology:
            if not section_predicate(section):
                continue

            if section.is_a_root_section():

                if distance < dist_to_section_distal[section]:
                    locations.append(MorphLocation(section=section, sectionpos=distance/dist_to_section_distal[section]) )

                else:

                    pass
            else:
                proximal_dist = dist_to_section_distal[section.parent]
                distal_dist = dist_to_section_distal[section]

                # Does a distance fall on this section:
                if proximal_dist <= distance < distal_dist:
                    prop = (distance - proximal_dist) / (distal_dist - proximal_dist)
                    assert 0.0 <= prop <= 1.0
                    locations.append(MorphLocation(section=section, sectionpos=prop))


        dummy = MorphLocation(morphology.get_dummy_section().children[0], 0.0)
        # Some sanity checking:
        for loc in locations:
            p = MorphPath(loc, dummy)
            assert np.fabs(p.get_length() - distance) < 0.01

        return locations

    @classmethod
    def get_locations_at_distances_away_from_dummy(cls, morphology, distances, section_predicate=None):
        return list(itertools.chain(*[cls.get_locations_at_distance_away_from_dummy(morphology, distance, section_predicate=section_predicate) for distance in distances] ))


