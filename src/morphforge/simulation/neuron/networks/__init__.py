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

from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.objects.neuronobject import NEURONObject
from Cheetah.Template import Template
from morphforge.simulation.base.networks import Synapse
from morphforge.simulation.base.networks import GapJunction
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.constants.standardtags import StandardTags

from morphforge.simulation.base import PostSynapticMechTemplate
from morphforge.simulation.base import PostSynapticMechInstantiation

class NEURONSynapse(NEURONObject, Synapse):

    def __init__(self, simulation, trigger, postsynaptic_mech, name=None, **kwargs):
        super(NEURONSynapse, self).__init__(simulation=simulation, trigger=trigger, postsynaptic_mech=postsynaptic_mech, name=name, **kwargs)


    def build_hoc(self, hocfile_obj):
        hocfile_obj[MHocFileData.Synapses][self] = {}
        # Build the pre and post component, if and only if they don't exist already:
        if not self._post_synaptic_mechanism in hocfile_obj[MHocFileData.Synapses]:
            self._post_synaptic_mechanism.build_hoc(hocfile_obj=hocfile_obj)
            assert self._post_synaptic_mechanism in hocfile_obj[MHocFileData.Synapses]

        if not (self,self._trigger) in hocfile_obj[MHocFileData.Synapses]:
            self._trigger.build_hoc_syn(hocfile_obj=hocfile_obj, synapse=self)
            assert  (self,self._trigger) in hocfile_obj[MHocFileData.Synapses]

    def build_mod(self, modfile_set):
        self._post_synaptic_mechanism.build_mod(modfile_set)
        self._trigger.build_mod(modfile_set)

    def get_recordable(self, what, **kwargs):
        if what == StandardTags.Conductance:
            what = Synapse.Recordables.SynapticConductance
        if what == StandardTags.Current:
            what = Synapse.Recordables.SynapticCurrent

        if what in [Synapse.Recordables.SynapticCurrent,
                    Synapse.Recordables.SynapticConductance,
                    StandardTags.NMDAVoltageDependancy,
                    StandardTags.NMDAVoltageDependancySS]:
            return self._post_synaptic_mechanism.get_recordable(what=what,
                    **kwargs)
        if what in ['g']:
            return self._post_synaptic_mechanism.get_recordable(what=what, **kwargs)

        assert False


_expr_tmpl = """
// Gap Junction [$name]
objref $name1
objref $name2
${cellname1}.internalsections[$sectionindex1] $name1 = new Gap ($sectionpos1)
${cellname2}.internalsections[$sectionindex2] $name2 = new Gap ($sectionpos2)

${name1}.r = $resistance.rescale("MOhm").magnitude
${name2}.r = $resistance.rescale("MOhm").magnitude

setpointer ${name1}.vgap,  ${cellname2}.internalsections[$sectionindex2].v($sectionpos2)
setpointer ${name2}.vgap,  ${cellname1}.internalsections[$sectionindex1].v($sectionpos1)

"""

gap_mod = """
NEURON {
    POINT_PROCESS Gap
    POINTER vgap
    RANGE r, i
    NONSPECIFIC_CURRENT i
}

PARAMETER{
    r = 1e10 (megohm)
}

ASSIGNED {
    v (millivolt)
    vgap (millivolt)
    i (nanoamp)
}
BREAKPOINT{
    i = (v-vgap)/r
    }

"""


class NEURONGapJunction(GapJunction, NEURONObject):

    def __init__(self, **kwargs):
        super(NEURONGapJunction, self).__init__(**kwargs)

    is_first_build = True

    def build_mod(self, modfile_set):

        if NEURONGapJunction.is_first_build:
            NEURONGapJunction.is_first_build = False
            modfile = ModFile(modtxt=gap_mod, name='GapJunction')
            modfile_set.append(modfile)

    def build_hoc(self, hocfile_obj):
        cell1 = self.celllocation1.cell
        cell2 = self.celllocation2.cell
        section1 = self.celllocation1.morphlocation.section
        section2 = self.celllocation2.morphlocation.section

        gp_obj1_name = self.get_name() + 'A'
        gp_obj2_name = self.get_name() + 'B'
        hoc_dct = hocfile_obj[MHocFileData.Cells]
        data = {
            'name': self.get_name(),
            'name1': gp_obj1_name,
            'name2': gp_obj2_name,
            'cell1': cell1,
            'cell2': cell2,
            'cellname1': hoc_dct[cell1]['cell_name'],
            'cellname2': hoc_dct[cell2]['cell_name'],
            'sectionindex1': hoc_dct[cell1]['section_indexer'][section1],
            'sectionindex2': hoc_dct[cell2]['section_indexer'][section2],
            'sectionpos1': self.celllocation1.morphlocation.sectionpos,
            'sectionpos2': self.celllocation2.morphlocation.sectionpos,
            'resistance': self.resistance,
            }

        hocfile_obj.add_to_section(MHOCSections.InitGapJunction,
                                   Template(_expr_tmpl, data).respond())

        hocfile_obj[MHocFileData.GapJunctions][self] = data

    def get_recordable(self, what, **kwargs):
        raise NotImplementedError()





class NEURONPostSynapticMechTemplate(PostSynapticMechTemplate):
    pass


from morphforge.simulation.base.base_classes import NamedSimulationObject





class NEURONPostSynapticMechInstantiation(PostSynapticMechInstantiation, NamedSimulationObject):
    def __init__(self, src_tmpl, _default_parameters, parameter_multipliers=None, parameter_overides=None,  **kwargs):
        super(NEURONPostSynapticMechInstantiation, self).__init__(does_require_simulation=False, **kwargs)
        self.src_tmpl = src_tmpl

        self._default_parameters = _default_parameters.copy()
        self.parameter_multipliers=parameter_multipliers or {}
        self.parameter_overides=parameter_overides or {}

    def get_resolved_parameters(self):
        # Resolve the parameters:
        params = self._default_parameters.copy()
        assert not (set(self.parameter_multipliers.keys()) & set(self.parameter_overides.keys()))

        for k,v in self.parameter_multipliers.iteritems():
            params[k] = params[k] * v

        for k,v in self.parameter_overides.iteritems():
            params[k] = v

        if not set( params.keys() ) == set( self.src_tmpl.get_variables() ):
            print params.keys(),  self.src_tmpl.get_variables() 
            print self.src_tmpl, type(self.src_tmpl)
            assert False

        return params


    def build_hoc(self, hocfile_obj):
        raise NotImplementedError()
    def build_mod(self, modfile_set):
        raise NotImplementedError()





class NEURONPostSynapticMechTemplateForwardToTemplate(NEURONPostSynapticMechTemplate):

    def __init__(self, **kwargs):
        super(NEURONPostSynapticMechTemplateForwardToTemplate, self).__init__(**kwargs)
        self.is_mod_built=False

    def template_build_mod_once(self, modfile_set):
        if not self.is_mod_built:
            self.is_mod_built=True
            return self.template_build_mod(modfile_set=modfile_set)

    def template_build_mod(self, modfile_set):
        raise NotImplementedError()

    def build_hoc_for_instance(self, instance, hocfile_obj):
        raise NotImplementedError()

    def get_record_for_instance(self, instance, **kwargs):
        raise NotImplementedError()

    def instantiate(self, parameter_multipliers=None, parameter_overrides=None, **kwargs):
        return NEURONPostSynapticMechInstantiationForwardToTemplate(
                src_tmpl=self, 
                _default_parameters=self._default_parameters,
                 parameter_multipliers=parameter_multipliers,
                 parameter_overides=parameter_overrides,
                 **kwargs
                )


class NEURONPostSynapticMechInstantiationForwardToTemplate(NEURONPostSynapticMechInstantiation):

    # The default behaviour is for instances to forward
    # responsbility back to thier parent:
    def build_hoc(self, hocfile_obj):
        return self.src_tmpl.build_hoc_for_instance(hocfile_obj=hocfile_obj, instance=self)

    def build_mod(self, modfile_set):
        return self.src_tmpl.template_build_mod_once(modfile_set=modfile_set)

    def get_recordable(self, **kwargs):
        return  self.src_tmpl.get_record_for_instance( instance=self, **kwargs)

