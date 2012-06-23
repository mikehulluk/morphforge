#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData, MHOCSections
from morphforgecontrib.simulation.synapses.core import PostSynapticMech_Exp2Syn
from Cheetah.Template import Template
from morphforge.simulation.neuron.networks import NeuronSynapse
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment


from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_CurrentRecord
from postsynaptic_mechanisms_baseclasses import Neuron_PSM_Std_ConductanceRecord
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.core import mfrandom

class Neuron_PSM_Exp2Syn_CurrentRecord(Neuron_PSM_Std_CurrentRecord):
    pass


class Neuron_PSM_Exp2Syn_ConductanceRecord(Neuron_PSM_Std_ConductanceRecord):
    pass







exp2HOCTmpl = """
// Post-Synapse [ $synnamepost ]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new Exp2SynMorphforge ( $sectionpos )
${synnamepost}.tau1 = $tau_open.rescale("ms").magnitude
${synnamepost}.tau2 = $tau_close.rescale("ms").magnitude
${synnamepost}.e = $e_rev.rescale("mV").magnitude
${synnamepost}.popening = $pOpening

"""

class Neuron_PSM_Exp2Syn(PostSynapticMech_Exp2Syn):

    def __init__(self, simulation,vdep, **kwargs):
        PostSynapticMech_Exp2Syn.__init__( self,  **kwargs)
        assert vdep==None




    def build_hoc(self, hocfile_obj):
        cell = self.celllocation.cell
        section = self.celllocation.morphlocation.section
        syn_name_post = self.synapse.get_name() + "Post"
        data = {
               "synnamepost":syn_name_post,
               "cell":cell,
               "cellname":hocfile_obj[MHocFileData.Cells][cell]['cell_name'],
               "sectionindex":hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section],
               "sectionpos":self.celllocation.morphlocation.sectionpos,

               "tau_open": self.tau_open,
               "tau_close": self.tau_close,
               "e_rev": self.e_rev,
               "pOpening": self.popening,

               }

        hocfile_obj.add_to_section( MHOCSections.InitSynapsesChemPost,  Template(exp2HOCTmpl, data).respond() )

        hocfile_obj[MHocFileData.Synapses][self.synapse] = {}
        hocfile_obj[MHocFileData.Synapses][self.synapse]["POST"] = data

    def build_mod(self, modfile_set):
        import postsynaptic_mechanisms_exp2syn_modfile
        modfile = ModFile(modtxt=postsynaptic_mechanisms_exp2syn_modfile.getExp2SynModfile(), name='UnusedParameterXXXExpSyn2')
        modfile_set.append(modfile)



    def get_recordable(self, what, **kwargs):
        if what == NeuronSynapse.Recordables.SynapticCurrent:
            return Neuron_PSM_Exp2Syn_CurrentRecord( neuron_syn_post=self, **kwargs)
        if what == NeuronSynapse.Recordables.SynapticConductance:
            return Neuron_PSM_Exp2Syn_ConductanceRecord( neuron_syn_post=self, **kwargs)
        assert False






#NeuronSimulationEnvironment.registerPostSynapticMechanism( PostSynapticMech_Exp2Syn, Neuron_PSM_Exp2Syn)
#NeuronSimulationEnvironment.registerPostSynapticMechanism( PostSynapticMech_ExpSyn, Neuron_PSM_ExpSyn)

NeuronSimulationEnvironment.postsynapticmechanisms.register_plugin(PostSynapticMech_Exp2Syn, Neuron_PSM_Exp2Syn)
