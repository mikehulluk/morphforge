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
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforge.simulation.neuron.biophysics.modfile import ModFile

from morphforge.core import ObjectLabeller
from Cheetah.Template import Template

from morphforge.simulation.neuron.networks import NEURONPostSynapticMechTemplateForwardToTemplate
from morphforge.stdimports import SummariserLibrary


import mredoc as mrd


from neurounits.neurounitparser import NeuroUnitParser
from neurounits.codegen.nmodl import WriteToNMODL, MechanismType



class NeuroUnitEqnsetPostSynaptic(object):
    def __init__(self, eqnset, default_parameters=None, recordables_map= None, recordables_data=None, **kwargs):
        super(NeuroUnitEqnsetPostSynaptic, self).__init__(**kwargs)

        if isinstance(eqnset, basestring):
            eqnset = NeuroUnitParser.Parse9MLFile(eqnset).get_component()

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


    def get_summary_description(self, instance=None):
        inst_details=''
        if instance:
            print instance.__dict__
            if instance.parameter_multipliers:
                inst_details += 'Multipliers: %s'%str(instance.parameter_multipliers)
            if instance.parameter_overides:
                inst_details += 'Overrides: %s'%str(instance.parameter_overides)
        return "<Defined through NeuroUnit: '%s' %s>"%( self.name, inst_details )







class NeuroUnitEqnsetPostSynapticSummariser(object):
    
    @classmethod
    def build(cls, obj):
        #child_elements = []
        
        
        
        eqnset_redoc = obj.eqnset.to_redoc()
        return mrd.Section('%s (Neurounit Synaptic-Template)' %obj.name, 
                eqnset_redoc, 
                cls._build_default_parameters(obj),
                mrd.Section('Source', mrd.VerbatimBlock(obj.eqnset.library_manager.src_text, caption='Source code for template: %s'% obj.name) )
                )
        
    @classmethod
    def _build_default_parameters(cls, obj):
        tbl = mrd.VerticalColTable('Parameter| Default Value',
            [ '%s|%s'%(str(k), str(v)) for (k,v) in obj._default_parameters.items() ] )
        return mrd.Section('Default Parameters', tbl)


SummariserLibrary.register_summariser( NeuroUnitEqnsetPostSynaptic, NeuroUnitEqnsetPostSynapticSummariser)







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


    def template_build_mod_once(self, modfile_set):
        if not self.is_mod_built:
            modfile_set.append(ModFile(modtxt=self.nmodl_txt, name='UnusedParameterXXXExpSyn2', strict_modlunit=True))
            self.is_mod_built = True

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


        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost, Template(exp2HOCTmpl, data).respond())
        assert not instance in hocfile_obj[MHocFileData.Synapses]
        hocfile_obj[MHocFileData.Synapses][instance] = data



NEURONEnvironment.synapse_psm_template_type.register_plugin(
        NeuroUnitEqnsetPostSynaptic, 
        NEURONPostSynapticTemplate_NeuroUnitEquationSetPostSynaptic )
        
