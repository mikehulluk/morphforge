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

from morphforge.simulation.base.biophysics import CellBiophysics

from morphforge.constants import StandardTags
from morphforge.core.quantities.fromcore import unit
from morphforge.simulation.base.base_classes import NamedSimulationObject
from morphforge.simulation.base.core.celllocation import CellLocation


class Cell(NamedSimulationObject):

    class Recordables(object):

        MembraneVoltage = StandardTags.Voltage

    @property
    def cell_type(self):
        return self._cell_type

    @property
    def cell_type_str(self):
        return (self._cell_type if self._cell_type else '<?>')


    def __init__(self,  morphology, segmenter=None, initial_voltage=None, cell_tags=None, cell_type=None, **kwargs):

        if cell_tags == None:
            cell_tags = []

        from morphforge.simulation.base.segmentation.cellsegmenter import CellSegmenter_MaxCompartmentLength
        super(Cell, self).__init__(**kwargs)

        self.morphology = morphology
        self._cell_type = cell_type

        self.cell_segmenter = (segmenter if segmenter else CellSegmenter_MaxCompartmentLength())
        self.cell_segmenter.connect_to_cell(self)

        self.biophysics = CellBiophysics()

        self.initial_voltage = initial_voltage or unit('-51:mV')

        self.cell_tags = cell_tags

        if self.name:
            self.cell_tags = self.cell_tags + [self.name]

        self.population = None


    @property
    def index_in_pop(self):
        assert self.population is not None
        return self.population.index(self)

    def get_location(self, idtag, sectionpos=0.5):
        return CellLocation(cell=self,
                            section=self.morphology.get_section(idtag=idtag),
                            sectionpos=sectionpos)

    def get_region(self, region_name):
        return self.morphology.get_region(region_name)

    def get_regions(self):
        return self.morphology.get_regions()

    def get_biophysics(self):
        return self.biophysics

    def get_segmenter(self):
        return self.cell_segmenter

    # Make the object a bit more pythonic:
    @property
    def segmenter(self):
        return self.cell_segmenter

    @property
    def presynaptic_connections(self):
        return [synapse for synapse in self.simulation.synapses
                if synapse.get_presynaptic_cell() == self]

    @property
    def postsynaptic_connections(self):
        return [synapse for synapse in self.simulation.synapses
                if synapse.get_postsynaptic_cell() == self]

    @property
    def electrical_connections(self):
        return [gap_junction for gap_junction in self.simulation.gapjunctions if self
                in gap_junction.connected_cells]


    # Commonly used helper methods:
    @property
    def soma(self):
        return self.get_location('soma')

    @property 
    def is_single_compartment(self):
        return len( self.morphology ) == 1 and \
               self.segmenter.get_num_segments(self.soma.section) == 1


