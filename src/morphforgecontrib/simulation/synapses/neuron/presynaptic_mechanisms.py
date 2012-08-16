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


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData,\
    MHOCSections
from Cheetah.Template import Template
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_VoltageThreshold, PreSynapticMech_TimeList







preTmpl = """
// Pre-Synapse [ $synname ]
objref $synnamepre
${cellname}.internalsections[$sectionindex] $synnamepre = new NetCon( &v($sectionpos), $synnamepost, $threshold.rescale("mV").magnitude, $delay.rescale("ms").magnitude, $weight.rescale("uS").magnitude  )
"""

class NeuronSynapseTriggerVoltageThreshold(PreSynapticMech_VoltageThreshold):


    def build_hoc(self, hocfile_obj):
        cell =self.cell_location.cell
        section = self.cell_location.morphlocation.section
        syn_name = self.synapse.get_name()
        syn_name_post = hocfile_obj[MHocFileData.Synapses][self.synapse]["POST"]["synnamepost"]
        syn_name_pre = self.synapse.get_name() + "Pre"


        hoc_data = hocfile_obj[MHocFileData.Cells][cell]
        data = {
               "synname": syn_name,
               "synnamepost": syn_name_post,
               "synnamepre": syn_name_pre,
               "cell": cell,
               "cellname": hoc_data['cell_name'],
               "sectionindex": hoc_data['section_indexer'][section],
               "sectionpos": self.cell_location.morphlocation.sectionpos,
               "threshold": self.voltage_threshold ,
               "delay": self.delay,
               "weight": self.weight,
               }

        hocfile_obj.add_to_section( MHOCSections.InitSynapsesChemPre,  Template(preTmpl, data).respond() )

        hocfile_obj[MHocFileData.Synapses][self.synapse]["PRE"] = data


    def build_mod(self, modfile_set):
        pass











preTmplList = """
// Pre-Synapse [ $synname ]
objref ${synnamepre}_NullObj
objref $synnamepre
$synnamepre = new NetCon( ${synnamepre}_NullObj, $synnamepost, 0, 0, $weight.rescale("uS").magnitude  )


objref fih_${synnamepre}
fih_${synnamepre} = new FInitializeHandler("loadqueue_${synnamepre}()")
proc loadqueue_${synnamepre}() {
#for $event in $timelist:
${synnamepre}.event( $event.get_time.rescale("ms").magnitude )
#end for
}


"""

class NeuronSynapseTriggerTimeList(PreSynapticMech_TimeList):

    def build_hoc(self, hocfile_obj):
        hoc_data = hocfile_obj[MHocFileData.Synapses][self.synapse]
        syn_name = self.synapse.get_name()
        syn_name_post = hoc_data["POST"]["synnamepost"]
        syn_name_pre = self.synapse.get_name() + "Pre"

        data = {
               "synname": syn_name,
               "synnamepost" : syn_name_post,
               "synnamepre": syn_name_pre,
               "timelist": self.time_list,
               "weight": self.weight,
               }

        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPre,
                                   Template(preTmplList,
                                   data).respond())
        hocfile_obj[MHocFileData.Synapses][self.synapse]['PRE'] = data


    def build_mod(self, modfile_set):
        pass


#NeuronSimulationEnvironment.registerPreSynapticMechanism( PreSynapticMech_VoltageThreshold, NeuronSynapseTriggerVoltageThreshold)
#NeuronSimulationEnvironment.registerPreSynapticMechanism( PreSynapticMech_TimeList, NeuronSynapseTriggerTimeList)

NeuronSimulationEnvironment.presynapticmechanisms.register_plugin(PreSynapticMech_VoltageThreshold, NeuronSynapseTriggerVoltageThreshold)
NeuronSimulationEnvironment.presynapticmechanisms.register_plugin(PreSynapticMech_TimeList, NeuronSynapseTriggerTimeList)


