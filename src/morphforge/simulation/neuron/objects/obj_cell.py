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

from morphforge.core.quantities import unit

from neuronobject import NeuronObject
from morphforge.simulation.base import Cell

from morphforge.simulation.neuron.hocmodbuilders import HocBuilder
from morphforge.simulation.neuron.simulationdatacontainers import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable

from Cheetah.Template import Template
from morphforge.constants.standardtags import StandardTags


class MembraneVoltageRecord(NeuronRecordable):

    initial_buffer_size = 50000

    tmplObjRef = """
objref $recVecName
$recVecName = new Vector()
${recVecName}.buffer_size(%d)
${recVecName}.record(& ${cellname}.internalsections[${sectionindex}].v ($sectionpos))
    """%initial_buffer_size

    def __init__(self, cell, cell_location=None, **kwargs):
        super(MembraneVoltageRecord, self).__init__(**kwargs)
        self.cell = cell
        self.cell_location = cell_location if cell_location is not None else cell.get_location("soma")



    def get_unit(self):
        return unit('mV')

    def get_std_tags(self):
        return [StandardTags.Voltage]

    def get_description(self):
        r = 'Vm %s' % self.cell_location.cell.name
        if self.cell_location.morphlocation.section.idtag
            r += ':%s' % self.cell_location.morphlocation.section.idtag
        return r

    def build_hoc(self, hocfile_obj):
        cell = self.cell_location.cell
        section = self.cell_location.morphlocation.section
        cell_name = hocfile_obj[MHocFileData.Cells][cell]['cell_name']
        section_index = hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section]


        tmpl_dict = {
            'recVecName': self.name,
            'cellname': cell_name,
            'sectionindex': section_index,
            'sectionpos': self.cell_location.morphlocation.sectionpos,
            }
        print tmpl_dict

        hocfile_obj.add_to_section(MHOCSections.InitRecords,  Template(MembraneVoltageRecord.tmplObjRef,tmpl_dict).respond())

        hocfile_obj[MHocFileData.Recordables][self] = tmpl_dict


    def build_mod(self, modfile_set):
        pass








class MNeuronCell(Cell, NeuronObject):
    def build_hoc(self, hocfile_obj):
        HocBuilder.Cell(hocfile_obj=hocfile_obj, cell=self)

    def build_mod(self, modfile_set):
        mechanisms = set([mta.mechanism for mta in
                         self.get_biophysics().appliedmechanisms])
        for m in mechanisms:
            m.create_modfile(modfile_set)

    def get_recordable(self, what, **kwargs):
        recordables = \
            {MNeuronCell.Recordables.MembraneVoltage: MembraneVoltageRecord}
        return recordables[what](cell=self, **kwargs)
