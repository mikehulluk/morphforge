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
from morphforge.simulation.neuron.biophysics.mm_neuron import NEURONChl_Base
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment

from neurounits.tools.nmodl import WriteToNMODL, MechanismType
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordable
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.membranemechanisms.common.neuron import build_hoc_default
from neurounits.neurounitparser import NeuroUnitParser

from morphforge.core import ObjectLabeller
from morphforge.simulation.base.networks import PostSynapticMech
from Cheetah.Template import Template






# WORK ON BUILDING TEMPLATES:
class NEURONPostSynapticTemplateInstantiation(PostSynapticMech):
    def __init__(self, src_tmpl,_default_parameters, parameter_multipliers=None, parameter_overides=None,  **kwargs):
        super(NEURONPostSynapticTemplateInstantiation, self).__init__(**kwargs)
        self.src_tmpl = src_tmpl

        self._default_parameters = _default_parameters.copy()
        self.parameter_multipliers=parameter_multipliers or {}
        self.parameter_overides=parameter_overides or {}

    def get_resolved_parameters(self):
        # Resolve the parameters:
        params = self._default_parameters.copy()
        assert not ( set(self.parameter_multipliers.keys()) & set(self.parameter_overides.keys()))

        for k,v in self.parameter_multipliers.iteritems():
            params[k] = params[k] * v

        for k,v in self.parameter_overides.iteritems():
            params[k] = v

        #print 'params', params
        #print 'expected_variables', self.src_tmpl.get_variables()
        assert set( params.keys() ) == set( self.src_tmpl.get_variables() )

        return params


    def build_hoc(self, hocfile_obj):
        raise NotImplementedError()

    def build_mod(self, modfile_set):
        return self.src_tmpl.template_build_mod(modfile_set=modfile_set)

class NEURONPostSynapticTemplate(object):

    def instantiate(self, **kwargs):
        raise NotImplementedError()

    def get_variables(self):
        raise NotImplementedError()






class RecordableData(object):

    def __init__(self, standard_tags=None):
        self.standard_tags = standard_tags or []


class NEURONChl_RecGen(NEURONRecordable):
    def __init__(self, src_chl, objvar, unit_in_nrn, std_tags, **kwargs):
        super(NEURONChl_RecGen, self).__init__(**kwargs)
        self.src_chl = src_chl
        self.objvar = objvar
        self.unit_in_nrn = unit_in_nrn
        self.std_tags = std_tags or []

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_object(
                hocfile_obj=hocfile_obj,
                vecname='RecVec%s' % self.name,
                objname=self.src_chl.synapse.get_name() + 'Post',
                objvar=self.objvar, recordobj=self)

    def get_description(self):
        return '%s %s' % (self.objvar, self.src_chl.name)

    def get_unit(self):
        return self.unit_in_nrn

    def get_std_tags(self):
        return self.std_tags




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
































class NEURONPostSynapticTemplateInstantiation_NeuroUnitEquationSetPostSynaptic(NEURONPostSynapticTemplateInstantiation):
    def __init__(self, **kwargs):
        super(NEURONPostSynapticTemplateInstantiation_NeuroUnitEquationSetPostSynaptic, self).__init__(**kwargs)

    def build_hoc(self, hocfile_obj):
        # Resolve the parameters for this instance:
        params = self.get_resolved_parameters()

        cell = self.cell_location.cell
        section = self.cell_location.morphlocation.section
        syn_name_post = self.synapse.get_name() + 'Post'
        cell_hoc = hocfile_obj[MHocFileData.Cells][cell]
        data = {
            'synnamepost': syn_name_post,
            'cell': cell,
            'cellname': cell_hoc['cell_name'],
            'sectionindex': cell_hoc['section_indexer'][section],
            'sectionpos': self.cell_location.morphlocation.sectionpos,
            'synapsetypename': self.src_tmpl.NRNSUFFIX,

            'parameters': [(k, float(v/self.src_tmpl.units[k])) for (k, v) in params.iteritems()]
               }

        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost,  Template(exp2HOCTmpl, data).respond())

        hocfile_obj[MHocFileData.Synapses][self.synapse] = {}
        hocfile_obj[MHocFileData.Synapses][self.synapse]['POST'] = data


class NEURONPostSynapticTemplate_NeuroUnitEquationSetPostSynaptic(NeuroUnitEqnsetPostSynaptic, NEURONPostSynapticTemplate):
    def __init__(self, template_name=None, **kwargs):
        super(NEURONPostSynapticTemplate_NeuroUnitEquationSetPostSynaptic, self).__init__( **kwargs)

        self.template_name =template_name
        self.is_mod_built = False

        self.nmodl_txt, self.buildparameters = WriteToNMODL(self.eqnset, neuron_suffix="NRNEQNSETSYN"+ObjectLabeller.get_next_unamed_object_name(type(self), prefix=""))

        assert self.buildparameters.mechanismtype == MechanismType.Point
        self.units = {}
        for (param_str, value) in self._default_parameters.iteritems():
            sym = self.eqnset.get_terminal_obj(param_str)
            param_default_unit = self.buildparameters.symbol_units[sym]
            self.units[param_str] = param_default_unit.as_quantities_unit()

        self.NRNSUFFIX = self.buildparameters.suffix

    def instantiate(self, parameter_multipliers=None, parameter_overides=None, **kwargs):
        return NEURONPostSynapticTemplateInstantiation_NeuroUnitEquationSetPostSynaptic(
                src_tmpl=self, 
                _default_parameters=self._default_parameters,
                 parameter_multipliers=parameter_multipliers,
                 parameter_overides=parameter_overides,
                 **kwargs
                )

    def template_build_mod(self, modfile_set):
        if not self.is_mod_built:
            modfile_set.append(ModFile(modtxt=self.nmodl_txt, name='UnusedParameterXXXExpSyn2'))
            self.is_mod_built = True



