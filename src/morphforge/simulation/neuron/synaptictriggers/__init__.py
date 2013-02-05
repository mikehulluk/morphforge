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
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforge.simulation.base.synaptictriggers import SynapticTriggerByVoltageThreshold, SynapticTriggerAtTimes



#preTmpl = """
#// Pre-Synapse  (will drive:[$synnames])
##for syn_name_post in $synnamespost:
#objref $(synnamepre)_$(syn_name_post)
#${cellname}.internalsections[$sectionindex] $(synnamepre)_$(syn_name_post) = new NetCon(&v($sectionpos), $syn_name_post, $threshold.rescale("mV").magnitude, $delay.rescale("ms").magnitude, 1.0 )
##end for
#"""

preTmpl = """
// Pre-Synapse  (will drive:[$synname])
objref $synname
${cellname}.internalsections[$sectionindex] $(synname) = new NetCon(&v($sectionpos), $synnamepost, $threshold.rescale("mV").magnitude, $delay.rescale("ms").magnitude, 1.0 )
"""

class NeuronSynapseTriggerVoltageThreshold(SynapticTriggerByVoltageThreshold):

    def build_hoc_syn(self, synapse, hocfile_obj):

        cell = self.cell_location.cell
        section = self.cell_location.morphlocation.section
        syn_name = synapse.get_name()

        #
        #print hocfile_obj[MHocFileData.Synapses].keys()

        synnamespost =  hocfile_obj[MHocFileData.Synapses][synapse.get_postsynaptic_mechanism()]['synnamepost']

        hoc_data = hocfile_obj[MHocFileData.Cells][cell]
        data = {
            'synname': syn_name,
            'synnamepost': synnamespost,
            'cell': cell,
            'cellname': hoc_data['cell_name'],
            'sectionindex': hoc_data['section_indexer'][section],
            'sectionpos': self.cell_location.morphlocation.sectionpos,
            'threshold': self.voltage_threshold,
            'delay': self.delay,
            }

        assert not (synapse,self) in hocfile_obj[MHocFileData.Synapses]
        hocfile_obj[MHocFileData.Synapses][(synapse,self)] = data
        text = Template(preTmpl, data).respond()
        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPre, text)



    def build_mod(self, modfile_set):
        pass


preTmplList = """
// Pre-Synapse, which drives the following: [$synname]
objref ${synnamepre}_NullObj
objref $synnamepre
$synnamepre = new NetCon(${synnamepre}_NullObj, $synnamepost, 0, 0, 1.0)


objref fih_${synnamepre}
fih_${synnamepre} = new FInitializeHandler("loadqueue_${synnamepre}()")
proc loadqueue_${synnamepre}() {
#for $event in $timelist:
${synnamepre}.event($event.get_time.rescale('ms').magnitude )
#end for
}


"""

class NeuronSynapseTriggerTimeList(SynapticTriggerAtTimes):

    def build_hoc_syn(self, hocfile_obj, synapse):
        syn_name = synapse.get_name()
        syn_name_post =  hocfile_obj[MHocFileData.Synapses][synapse.get_postsynaptic_mechanism()]['synnamepost']
        syn_name_pre = synapse.get_name() + 'Pre'

        data = {
            'synname': syn_name,
            'synnamepost': syn_name_post,
            'synnamepre': syn_name_pre,
            'timelist': self.time_list,
            }

        assert not (synapse,self) in hocfile_obj[MHocFileData.Synapses]
        hocfile_obj[MHocFileData.Synapses][(synapse,self)] = data
        text = Template(preTmplList, data).respond()
        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPre, text)



    def build_mod(self, modfile_set):
        pass


NEURONEnvironment.presynapticmechanisms.register_plugin(SynapticTriggerByVoltageThreshold, NeuronSynapseTriggerVoltageThreshold)
NEURONEnvironment.presynapticmechanisms.register_plugin(SynapticTriggerAtTimes, NeuronSynapseTriggerTimeList)


