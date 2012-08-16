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


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData, MHOCSections
from morphforgecontrib.simulation.synapses.core import PostSynapticMech_Exp2SynNMDA
from Cheetah.Template import Template
from morphforge.simulation.neuron.networks import NeuronSynapse, Synapse
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NeuronSimulationEnvironment


from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_CurrentRecord
from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_ConductanceRecord
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.core.mfrandom import MFRandom
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.core.quantities.fromcore import unit
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils

import postsynaptic_mechanisms_exp2syn_nmda_modfile


class Neuron_PSM_Exp2SynNMDA_CurrentRecord(Neuron_PSM_Std_CurrentRecord):
    pass


class Neuron_PSM_Exp2SynNMDA_ConductanceRecord(Neuron_PSM_Std_ConductanceRecord):
    pass


class Neuron_PSM_Std_NMDAVoltageDependanceRecord(NeuronRecordable):

    def __init__(self, neuron_syn_post, **kwargs):
        super(Neuron_PSM_Std_NMDAVoltageDependanceRecord,
              self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

    def get_unit(self):
        return unit('')
    def get_std_tags(self):
        return [StandardTags.NMDAVoltageDependancy]

    def build_hoc(self, hocfile_obj):
        obj_name_hoc = hocfile_obj[MHocFileData.Synapses][self.neuron_syn_post.synapse]["POST"]["synnamepost"]
        HocModUtils.create_record_from_object( hocfile_obj=hocfile_obj, vecname="RecVec%s"%self.name, objname=obj_name_hoc, objvar="voltage_dependancy", recordobj=self )

    def build_mod(self, modfile_set):
        pass




exp2HOCTmpl = """
// Post-Synapse [ $synnamepost ]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new Exp2SynNMDAMorphforge ( $sectionpos )
${synnamepost}.tau1 = $tau_open.rescale("ms").magnitude
${synnamepost}.tau2 = $tau_close.rescale("ms").magnitude
${synnamepost}.e = $e_rev.rescale("mV").magnitude
${synnamepost}.popening = $pOpening

"""

class Neuron_PSM_Exp2SynNMDA(PostSynapticMech_Exp2SynNMDA):


    def __init__(self, simulation, **kwargs):
        PostSynapticMech_Exp2SynNMDA.__init__( self,  **kwargs)




    def build_hoc(self, hocfile_obj):
        cell = self.cell_location.cell
        section = self.cell_location.morphlocation.section
        syn_name_post = self.synapse.get_name() + "Post"
        data = {
               "synnamepost":syn_name_post,
               "cell":cell,
               "cellname":hocfile_obj[MHocFileData.Cells][cell]['cell_name'],
               "sectionindex":hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section],
               "sectionpos":self.cell_location.morphlocation.sectionpos,

               "tau_open": self.tau_open,
               "tau_close": self.tau_close,
               "e_rev": self.e_rev,
               "pOpening": self.popening,
               'random_seed': MFRandom.get_seed(),
               }

        hocfile_obj.add_to_section( MHOCSections.InitSynapsesChemPost,  Template(exp2HOCTmpl, data).respond() )

        hocfile_obj[MHocFileData.Synapses][self.synapse] = {}
        hocfile_obj[MHocFileData.Synapses][self.synapse]["POST"] = data

    def build_mod(self, modfile_set):


        modfile = ModFile(modtxt=postsynaptic_mechanisms_exp2syn_nmda_modfile.get_exp2_syn_nmda_modfile(vdep=self.vdep), name='UnusedParameterXXXExpSyn2')
        modfile_set.append(modfile)



    def get_recordable(self, what, **kwargs):
        if what == Synapse.Recordables.SynapticCurrent:
            return Neuron_PSM_Exp2SynNMDA_CurrentRecord( neuron_syn_post=self, **kwargs)
        if what == Synapse.Recordables.SynapticConductance:
            return Neuron_PSM_Exp2SynNMDA_ConductanceRecord( neuron_syn_post=self, **kwargs)
        if what == StandardTags.NMDAVoltageDependancy:
            return Neuron_PSM_Std_NMDAVoltageDependanceRecord( neuron_syn_post=self, **kwargs)
        assert False






#NeuronSimulationEnvironment.registerPostSynapticMechanism( PostSynapticMech_Exp2SynNMDA, Neuron_PSM_Exp2SynNMDA)
NeuronSimulationEnvironment.postsynapticmechanisms.register_plugin(PostSynapticMech_Exp2SynNMDA, Neuron_PSM_Exp2SynNMDA)

