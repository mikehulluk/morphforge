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

from morphforge.morphology.core import MorphologyTree, Section, Region
import numpy
import quantities as pq
from morphforge.core.misc import is_float, is_int
import morphforge
from morphforge.core.quantities.fromcore import unit


# pylint: disable=E1103
# pylint tries to work out the return value of _convert_to_unit,
# but does it wrong and makes complaints.

def _convert_to_unit(o, default_unit):

    assert not isinstance(default_unit, pq.quantity.Quantity)

    if isinstance(o, pq.quantity.Quantity):
        return o.rescale(default_unit)
    elif is_float(o) or is_int(o):
        return o * morphforge.core.quantities.unit_string_parser.parse(default_unit).rescale(default_unit)
    elif isinstance(o, (str, unicode)) and ':' in o:
        return unit(o).rescale(default_unit)
    else:
        raise ValueError()


class MorphologyBuilder(object):

    """ Class to build simple neuron morphologies """

    @classmethod
    def get_single_section_soma(cls, rad=None, area=None):
        assert (rad or area) and not (rad and area)

        if area:
            area = _convert_to_unit(area, default_unit="um2").rescale("um2").magnitude
            rad = numpy.power((area / (4.0 * numpy.pi)), 1.0 / 2.0)

        else:
            assert isinstance(rad, int) or isinstance(rad, float)
            rad = _convert_to_unit(rad, default_unit="um").rescale("um").magnitude

        soma_region = Region("soma")
        dummysection = Section(region=None, x=0.0, y=0.0, z=0.0, r=rad)
        dummysection.create_distal_section(region=soma_region, x=rad * 2.0, y=0.0, z=0.0, r=rad, idtag="soma")
        cell = MorphologyTree("SimpleSomaMorph", dummysection=dummysection, metadata={})
        return cell

    @classmethod
    def get_soma_axon_morph(cls, axon_length=1000.0, axon_radius=0.3, soma_radius=20.0, axon_sections=10):
        soma_region = Region("soma")
        axon_region = Region("axon")

        axon_section_length = float(axon_length) / float(axon_sections)
        dummy_root = Section(region=None, x=0.0, y=0.0, z=0.0, r=soma_radius)
        soma = dummy_root.create_distal_section(region=soma_region, x=soma_radius * 2.0, y=0.0, z=0.0, r=soma_radius, idtag="soma")
        prev_section = soma
        for x in range(1, axon_sections):
            axon = prev_section.create_distal_section(region=axon_region, x=x * axon_section_length + 2.0 * soma_radius, y=0, z=0, r=axon_radius, idtag="axon_%d" % x)
            prev_section = axon
        cell = MorphologyTree('SimpleSomaAxonMorph',
                              dummysection=dummy_root, metadata={})
        return cell


