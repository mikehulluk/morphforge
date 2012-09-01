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

from Cheetah.Template import Template


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordableOnLocation
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils


class MM_Neuron_GeneralisedRecord(NEURONRecordableOnLocation):
    def __init__(self, modvar, unit, tags, nrnsuffix, **kwargs):
        super(MM_Neuron_GeneralisedRecord, self).__init__(**kwargs)
        self.unit = unit
        self.tags = tags
        self.modvar = modvar
        self.nrnsuffix = nrnsuffix

    def get_unit(self):
        return self.unit

    def get_std_tags(self):
        return self.tags

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile(
            hocfile_obj,
            vecname='RecVec%s' % self.name,
            cell_location=self.cell_location,
            modvariable=self.modvar,
            mod_neuronsuffix=self.nrnsuffix,
            recordobj=self,
           )








chlHoc = """

$(cell_name).internalsections [$section_index] {
    // Eqnset Channels
    insert $neuron_suffix
    #for variable_name, variable_value_nounit, variable_value_with_unit, variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //(in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""



def build_hoc_default(cell, section, hocfile_obj, mta,  units, nrnsuffix):

    cell_hoc = hocfile_obj[MHocFileData.Cells][cell]
    cell_name = cell_hoc['cell_name']
    section_index = cell_hoc['section_indexer'][section]

    # Calculate the values of the variables for the section:
    variables = []
    for variable_name in mta.mechanism.get_variables():
        variable_value_with_unit = mta.applicator.get_variable_value_for_section(variable_name=variable_name, section=section)
        variable_unit = units[variable_name]
        variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude
        variables.append([variable_name, variable_value_nounit, variable_value_with_unit, variable_unit])

    tmpl_dict = {
        'cell_name': cell_name,
        'section_index': section_index,
        'neuron_suffix': nrnsuffix,
        'variables': variables,
        }

    # Add the data to the HOC file
    hoc_text = Template(chlHoc, tmpl_dict).respond()
    hocfile_obj.add_to_section(MHOCSections.InitCellMembranes,
                               hoc_text)


