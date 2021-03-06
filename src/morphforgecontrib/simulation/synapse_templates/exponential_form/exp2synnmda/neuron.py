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


from .core import PostSynapticMech_Exp2SynNMDA_Base


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment

from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordable
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils

from Cheetah.Template import Template


from morphforge.simulation.neuron.networks import NEURONPostSynapticMechTemplateForwardToTemplate

from morphforge.stdimports import MFRandom
from morphforge.units import parse_unit_str

from morphforge.stdimports import StandardTags
from morphforgecontrib.simulation.synapse_templates.exponential_form.neuron_records import Neuron_PSM_Std_CurrentRecord
from morphforgecontrib.simulation.synapse_templates.exponential_form.neuron_records import Neuron_PSM_Std_ConductanceRecord
from morphforge.simulation.neuron.networks import NEURONSynapse


class Neuron_PSM_Std_NMDAVoltageDependanceRecord(NEURONRecordable):

    def __init__(self, neuron_syn_post, **kwargs):

        super(Neuron_PSM_Std_NMDAVoltageDependanceRecord, self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

        self._description="MyDesc!!"

    def get_unit(self):
        return parse_unit_str('')

    def get_std_tags(self):
        return [StandardTags.NMDAVoltageDependancy]

    def build_hoc(self, hocfile_obj):
        assert len(self.neuron_syn_post.synapses) == 1
        obj_name_hoc = hocfile_obj[MHocFileData.Synapses][self.neuron_syn_post]["synnamepost"]
        HocModUtils.create_record_from_object(hocfile_obj=hocfile_obj, vecname="RecVec%s" % self.name, objname=obj_name_hoc, objvar="voltage_dependancy", recordobj=self)

    def build_mod(self, modfile_set):
        pass

class Neuron_PSM_Std_NMDAConductanceWithVoltageDependanceRecord(NEURONRecordable):

    def __init__(self, neuron_syn_post, **kwargs):

        super(Neuron_PSM_Std_NMDAConductanceWithVoltageDependanceRecord, self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

    def get_unit(self):
        return parse_unit_str('uS')

    def get_std_tags(self):
        return [StandardTags.NMDAConductanceWithVDep]

    def build_hoc(self, hocfile_obj):
        assert len(self.neuron_syn_post.synapses) == 1
        obj_name_hoc = hocfile_obj[MHocFileData.Synapses][self.neuron_syn_post]["synnamepost"]
        HocModUtils.create_record_from_object(hocfile_obj=hocfile_obj, vecname="RecVec%s" % self.name, objname=obj_name_hoc, objvar="gtot", recordobj=self)

    def build_mod(self, modfile_set):
        pass


exp2HOCTmpl = """
// Post-Synapse [$synnamepost]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new Exp2SynNMDAMorphforge ($sectionpos)
${synnamepost}.tau1 = $tau_open.rescale("ms").magnitude
${synnamepost}.tau2 = $tau_close.rescale("ms").magnitude
${synnamepost}.e = $e_rev.rescale("mV").magnitude
${synnamepost}.popening = $pOpening
${synnamepost}.is_vdep_on = $is_vdep_on
${synnamepost}.peak_conductance = $peak_conductance.rescale('uS').magnitude

${synnamepost}.is_conductance_limited_on = $is_conductance_limited_on
${synnamepost}.conductance_limit = $conductance_limit
${synnamepost}.gamma = $gamma.rescale('per_mV').magnitude
${synnamepost}.eta = $eta.rescale('per_mM').magnitude
${synnamepost}.mg2conc = $mg2conc.rescale('mM').magnitude
"""


class NEURONPostSynapticMechTemplate_Exp2SynNMDA(PostSynapticMech_Exp2SynNMDA_Base, NEURONPostSynapticMechTemplateForwardToTemplate):

    def __init__(self, **kwargs):
        super(NEURONPostSynapticMechTemplate_Exp2SynNMDA, self).__init__(**kwargs)

    def build_hoc_for_instance(self, instance, hocfile_obj):

        params = instance.get_resolved_parameters()
        tau_open = params['tau_open']
        tau_close = params['tau_close']
        e_rev = params['e_rev']
        popening = params['popening']
        vdep = params['vdep']
        limit_conductance = params['limit_conductance']
        peak_conductance = params['peak_conductance']

        gamma = params['gamma']
        eta = params['eta']
        mg2conc = params['mg2conc']

        cell = instance.cell_location.cell
        section = instance.cell_location.morphlocation.section
        syn_name_post = instance.name + 'Post'
        hoc_data_cell = hocfile_obj[MHocFileData.Cells][cell]
        data = {
            'synnamepost': syn_name_post,
            'cell': cell,
            'cellname': hoc_data_cell['cell_name'],
            'sectionindex': hoc_data_cell['section_indexer'][section],
            'sectionpos': instance.cell_location.morphlocation.sectionpos,
            'tau_open': tau_open,
            'tau_close': tau_close,
            'e_rev': e_rev,
            'pOpening': popening,
            'random_seed': MFRandom.get_seed(),
            'is_vdep_on': (1.0 if vdep else 0.0),
            'is_conductance_limited_on': (1.0 if limit_conductance not in [None,False] else 0.0),
            'conductance_limit': (limit_conductance if limit_conductance not in [None,False] else -1.0),
            'peak_conductance': peak_conductance,
            'gamma':gamma,
            'eta':eta,
            'mg2conc':mg2conc,

               }

        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost,
                                   Template(exp2HOCTmpl, data).respond())

        assert not instance in hocfile_obj[MHocFileData.Synapses]
        hocfile_obj[MHocFileData.Synapses][instance] = data


    def template_build_mod(self, modfile_set):
        import postsynaptic_mechanisms_exp2syn_nmda_modfile_new
        modfile = ModFile(modtxt=postsynaptic_mechanisms_exp2syn_nmda_modfile_new.get_exp2_syn_nmda_modfile(), name='UnusedParameterXXXExpSyn2', strict_modlunit=True)
        modfile_set.append(modfile)

    def get_record_for_instance(self, instance, what, **kwargs):
        if what == NEURONSynapse.Recordables.SynapticCurrent:
            return Neuron_PSM_Std_CurrentRecord(neuron_syn_post=instance, **kwargs)
        if what == NEURONSynapse.Recordables.SynapticConductance:
            return Neuron_PSM_Std_ConductanceRecord(neuron_syn_post=instance, **kwargs)
        if what == StandardTags.NMDAVoltageDependancy:
            return Neuron_PSM_Std_NMDAVoltageDependanceRecord(neuron_syn_post=instance, **kwargs)
        if what == StandardTags.NMDAVoltageDependancy:
            return Neuron_PSM_Std_NMDAVoltageDependanceRecord(neuron_syn_post=instance, **kwargs)
        if what == StandardTags.NMDAConductanceWithVDep:
            return Neuron_PSM_Std_NMDAConductanceWithVoltageDependanceRecord(neuron_syn_post=instance, **kwargs)
        assert False




NEURONEnvironment.synapse_psm_template_type.register_plugin(PostSynapticMech_Exp2SynNMDA_Base, NEURONPostSynapticMechTemplate_Exp2SynNMDA)


