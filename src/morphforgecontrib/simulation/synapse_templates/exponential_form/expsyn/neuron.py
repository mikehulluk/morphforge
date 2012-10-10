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


from .core import PostSynapticMech_ExpSyn_Base


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment

from morphforge.simulation.neuron.biophysics.modfile import ModFile
from Cheetah.Template import Template
from morphforge.simulation.neuron.networks import NEURONPostSynapticMechTemplateForwardToTemplate

from morphforge.simulation.neuron.networks import NEURONSynapse

from morphforgecontrib.simulation.synapse_templates.exponential_form.neuron_records import Neuron_PSM_Std_CurrentRecord
from morphforgecontrib.simulation.synapse_templates.exponential_form.neuron_records import Neuron_PSM_Std_ConductanceRecord










_expr_tmpl = """
// Post-Synapse [$synnamepost]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new ExpSynMorphforge ($sectionpos)
${synnamepost}.tau = $tau.rescale("ms").magnitude
${synnamepost}.e = $e_rev.rescale("mV").magnitude
"""



class NEURONPostSynapticMechTemplate_ExpSyn(PostSynapticMech_ExpSyn_Base, NEURONPostSynapticMechTemplateForwardToTemplate):




    def __init__(self, **kwargs):
        print kwargs
        super(NEURONPostSynapticMechTemplate_ExpSyn, self).__init__( **kwargs)

    def build_hoc_for_instance(self, instance, hocfile_obj):

        params = instance.get_resolved_parameters()
        tau = params['tau']
        e_rev = params['e_rev']


        cell = instance.cell_location.cell
        section = instance.cell_location.morphlocation.section
        syn_name_post = instance.synapse.get_name() + 'Post'
        hoc_data_cell = hocfile_obj[MHocFileData.Cells][cell]
        data = {
               "synnamepost": syn_name_post,
               "cell": cell,
               "cellname": hoc_data_cell['cell_name'],
               "sectionindex": hoc_data_cell['section_indexer'][section],
               "sectionpos": instance.cell_location.morphlocation.sectionpos,

               "tau":   tau,
               "e_rev": e_rev,
               }


        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost,
                                   Template(_expr_tmpl, data).respond())

        hocfile_obj[MHocFileData.Synapses][instance.synapse] = {}
        hocfile_obj[MHocFileData.Synapses][instance.synapse]['POST'] = data


    def template_build_mod(self, modfile_set):
        import postsynaptic_mechanisms_expsyn_modfile
        modfile_set.append( ModFile(modtxt=postsynaptic_mechanisms_expsyn_modfile.getExpSynModfile(), name='UnusedParameterXXXExpSyn'))
        #self.is_mod_built = True

    def get_record_for_instance(self, instance, what, **kwargs):
        if what == NEURONSynapse.Recordables.SynapticCurrent:
            return Neuron_PSM_Std_CurrentRecord(neuron_syn_post=instance, **kwargs)
        if what == NEURONSynapse.Recordables.SynapticConductance:
            return Neuron_PSM_Std_ConductanceRecord(neuron_syn_post=instance, **kwargs)
        assert False


NEURONEnvironment.synapse_psm_template_type.register_plugin(PostSynapticMech_ExpSyn_Base, NEURONPostSynapticMechTemplate_ExpSyn)







