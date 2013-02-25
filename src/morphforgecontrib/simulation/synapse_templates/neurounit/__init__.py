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
#from morphforge.simulation.neuron.biophysics.mm_neuron import NEURONChl_Base
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment

from neurounits.tools.nmodl import WriteToNMODL, MechanismType
from morphforge.simulation.neuron.biophysics.modfile import ModFile
#from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordable
#from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
#from morphforgecontrib.simulation.channels.common.neuron import build_hoc_default
from neurounits.neurounitparser import NeuroUnitParser

from morphforge.core import ObjectLabeller
#from morphforge.simulation.base.networks import PostSynapticMech
from Cheetah.Template import Template


#from morphforge.simulation.base import PostSynapticMechTemplate
#from morphforge.simulation.base import PostSynapticMechInstantiation

#from morphforge.simulation.neuron.networks import NEURONPostSynapticMechInstantiation
#from morphforge.simulation.neuron.networks import NEURONPostSynapticMechTemplate

#from morphforge.simulation.neuron.networks import NEURONPostSynapticMechInstantiationForwardToTemplate
from morphforge.simulation.neuron.networks import NEURONPostSynapticMechTemplateForwardToTemplate




#~ 
#~ 
#~ class RecordableData(object):
#~ 
    #~ def __init__(self, standard_tags=None):
        #~ self.standard_tags = standard_tags or []
#~ 
#~ 
#~ class NEURONChl_RecGen(NEURONRecordable):
    #~ def __init__(self, src_chl, objvar, unit_in_nrn, std_tags, **kwargs):
        #~ super(NEURONChl_RecGen, self).__init__(**kwargs)
        #~ self.src_chl = src_chl
        #~ self.objvar = objvar
        #~ self.unit_in_nrn = unit_in_nrn
        #~ self.std_tags = std_tags or []
#~ 
    #~ def build_mod(self, modfile_set):
        #~ pass
#~ 
    #~ def build_hoc(self, hocfile_obj):
        #~ HocModUtils.create_record_from_object(
                #~ hocfile_obj=hocfile_obj,
                #~ vecname='RecVec%s' % self.name,
                #~ objname=self.src_chl.synapse.get_name() + 'Post',
                #~ objvar=self.objvar, recordobj=self)
#~ 
    #~ def get_description(self):
        #~ return '%s %s' % (self.objvar, self.src_chl.name)
#~ 
    #~ def get_unit(self):
        #~ return self.unit_in_nrn
#~ 
    #~ def get_std_tags(self):
        #~ return self.std_tags











class NeuroUnitEqnsetPostSynaptic(object):
    def __init__(self, eqnset, default_parameters=None, recordables_map= None, recordables_data=None, **kwargs):
        super(NeuroUnitEqnsetPostSynaptic, self).__init__(**kwargs)

        if isinstance(eqnset, basestring):
            eqnset = NeuroUnitParser.EqnSet(eqnset)

        self.eqnset = eqnset
        self._default_parameters = default_parameters or {}
        self.recordables_map = recordables_map or {}
        self.recordables_data = recordables_data or {}

        for param in eqnset.parameters:
            print param
            print param.symbol
            print 'iii', param.get_dimension().as_quantities_unit(), type(param.get_dimension().as_quantities_unit())
            print "iiii", self._default_parameters[param.symbol], type(self._default_parameters[param.symbol])
            assert param.symbol in self._default_parameters
            assert (param.get_dimension().as_quantities_unit() / self._default_parameters[param.symbol]).rescale("")

    def get_variables(self):
        return [p.symbol for p in self.eqnset.parameters]

















exp2HOCTmpl = """
// Post-Synapse [$synnamepost]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new $synapsetypename ($sectionpos)
#for param_name, param_value in $parameters:
    $(synnamepost).$(param_name) = $param_value      // $param_value
#end for

"""


class NEURONPostSynapticTemplate_NeuroUnitEquationSetPostSynaptic(NeuroUnitEqnsetPostSynaptic, NEURONPostSynapticMechTemplateForwardToTemplate):
    def __init__(self, **kwargs):
        super(NEURONPostSynapticTemplate_NeuroUnitEquationSetPostSynaptic, self).__init__( **kwargs)


        self.is_mod_built = False

        self.nmodl_txt, self.buildparameters = WriteToNMODL(self.eqnset, neuron_suffix="NRNEQNSETSYN"+ObjectLabeller.get_next_unamed_object_name(type(self), prefix=""))

        assert self.buildparameters.mechanismtype == MechanismType.Point
        self.units = {}
        for (param_str, value) in self._default_parameters.iteritems():
            sym = self.eqnset.get_terminal_obj(param_str)
            param_default_unit = self.buildparameters.symbol_units[sym]
            self.units[param_str] = param_default_unit.as_quantities_unit()

        self.NRNSUFFIX = self.buildparameters.suffix

    #def template_build_mod(self, modfile_set):
    #    if not self.is_mod_built:
    #        modfile_set.append(ModFile(modtxt=self.nmodl_txt, name='UnusedParameterXXXExpSyn2'))
    #        self.is_mod_built = True

    def template_build_mod_once(self, modfile_set):
        if not self.is_mod_built:
            modfile_set.append(ModFile(modtxt=self.nmodl_txt, name='UnusedParameterXXXExpSyn2', strict_modlunit=True))
            self.is_mod_built = True
        #self.template_build_mod( modfile_set)

    def build_hoc_for_instance(self, instance, hocfile_obj):
        # Resolve the parameters for this instance:
        params = instance.get_resolved_parameters()

        cell = instance.cell_location.cell
        section = instance.cell_location.morphlocation.section
        syn_name_post = instance.name + 'Post'
        cell_hoc = hocfile_obj[MHocFileData.Cells][cell]
        data = {
            'synnamepost': syn_name_post,
            'cell': cell,
            'cellname': cell_hoc['cell_name'],
            'sectionindex': cell_hoc['section_indexer'][section],
            'sectionpos': instance.cell_location.morphlocation.sectionpos,
            'synapsetypename': instance.src_tmpl.NRNSUFFIX,

            'parameters': [(k, float(v/instance.src_tmpl.units[k])) for (k, v) in params.iteritems()]
               }

        #hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost,  Template(exp2HOCTmpl, data).respond())

        #hocfile_obj[MHocFileData.Synapses][instance.synapse] = {}
        #hocfile_obj[MHocFileData.Synapses][instance.synapse]['POST'] = data

        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost, Template(exp2HOCTmpl, data).respond())
        assert not instance in hocfile_obj[MHocFileData.Synapses]
        hocfile_obj[MHocFileData.Synapses][instance] = data



NEURONEnvironment.synapse_psm_template_type.register_plugin(
        NeuroUnitEqnsetPostSynaptic, 
        NEURONPostSynapticTemplate_NeuroUnitEquationSetPostSynaptic )
