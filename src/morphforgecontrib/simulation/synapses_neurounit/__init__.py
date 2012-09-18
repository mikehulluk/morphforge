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


class NeuroUnitEqnsetPostSynaptic(PostSynapticMech):
    def __init__(self, cell_location, eqnset, default_parameters={}, recordables_map= None, recordables_data=None, name=None):
        PostSynapticMech.__init__(self, cell_location=cell_location)

        if isinstance(eqnset, basestring):
            eqnset = NeuroUnitParser.EqnSet(eqnset)

        self.name = name if name else ObjectLabeller.get_next_unamed_object_name(Neuron_NeuroUnitEqnsetPostSynaptic)
        self._parameters = default_parameters
        self.eqnset = eqnset
        self.recordables_map = recordables_map or {}
        self.recordables_data = recordables_data or {}

        for param in eqnset.parameters:
            print param
            print param.symbol
            print 'iii', param.get_dimension().as_quantities_unit(), type(param.get_dimension().as_quantities_unit())
            print "iiii", default_parameters[param.symbol], type(default_parameters[param.symbol])
            assert param.symbol in default_parameters
            assert (param.get_dimension().as_quantities_unit() / default_parameters[param.symbol]).rescale("")



exp2HOCTmpl = """
// Post-Synapse [$synnamepost]
objref $synnamepost
${cellname}.internalsections[$sectionindex] $synnamepost = new $synapsetypename ($sectionpos)
#for param_name, param_value in $parameters:
    $(synnamepost).$(param_name) = $param_value      // $param_value
#end for

"""

class Neuron_NeuroUnitEqnsetPostSynaptic(NEURONChl_Base, NeuroUnitEqnsetPostSynaptic):


    def __init__(self, **kwargs):
        NEURONChl_Base.__init__(self)
        NeuroUnitEqnsetPostSynaptic.__init__(self, **kwargs)

        #self.nmodl_txt, self.buildparameters = WriteToNMODL(self.eqnset)
        self.nmodl_txt, self.buildparameters = WriteToNMODL(self.eqnset, neuron_suffix="NRNEQNSETSYN"+ObjectLabeller.get_next_unamed_object_name(Neuron_NeuroUnitEqnsetPostSynaptic, prefix=""))

        assert self.buildparameters.mechanismtype == MechanismType.Point
        self.units = {}
        for (param_str, value) in self._parameters.iteritems():
            sym = self.eqnset.get_terminal_obj(param_str)
            param_default_unit = self.buildparameters.symbol_units[sym]
            self.units[param_str] = param_default_unit.as_quantities_unit()

        self.NRNSUFFIX = self.buildparameters.suffix

    def build_hoc(self, hocfile_obj):
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
            'synapsetypename': self.NRNSUFFIX,

             'parameters': [(k, float(v/self.units[k])) for (k, v) in self._parameters.iteritems()]


               }

        hocfile_obj.add_to_section(MHOCSections.InitSynapsesChemPost,  Template(exp2HOCTmpl, data).respond())

        hocfile_obj[MHocFileData.Synapses][self.synapse] = {}
        hocfile_obj[MHocFileData.Synapses][self.synapse]['POST'] = data

    def build_mod(self, modfile_set):
        modfile = ModFile(modtxt=self.nmodl_txt,
                          name='UnusedParameterXXXExpSyn2')
        modfile_set.append(modfile)




    def build_hoc_section(self, cell, section, hocfile_obj, mta):
        build_hoc_default(cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta , units=self.units, nrnsuffix=self.buildparameters.suffix)

    def create_modfile(self, modfile_set):
        modfile_set.append(ModFile(name=self.name,
                                   modtxt=self.nmodl_txt))

    def get_mod_file_changeables(self):
        change_attrs = set(['name', "nmodl_txt", 'mechanism_id',  'recordables_map', 'buildparameters', 'units', 'recordables_data'])
        fixed_attrs = set(['mm_neuronNumber', 'cachedNeuronSuffix', 'eqnset', '_parameters'])
        print set(self.__dict__)
        assert set(self.__dict__) == fixed_attrs | change_attrs
        return dict ([(a, getattr(self, a)) for a in change_attrs])




    def get_recordables(self):
        return self._get_recordable_symbols()
        assert False

    def _get_recordable_symbols(self):
        return [s.symbol for s in list(self.eqnset.states)
                + list(self.eqnset.assignedvalues)
                + list(self.eqnset.suppliedvalues)
                + list(self.eqnset.parameters)]

    def get_recordable(self, what, **kwargs):

        # Map it through the recordables_map, so that we can alias to StandardTags:
        what = self.recordables_map.get(what, what)

        valid_symbols = self._get_recordable_symbols()
        if not what in valid_symbols:
            err ="Unknown record value: %s. Expecting one of: %s "%(what, valid_symbols)
            raise ValueError(err)

        obj = self.eqnset.get_terminal_obj(what)
        unit_in_nrn = self.buildparameters.symbol_units[obj].as_quantities_unit()

        std_tags = []
        if what in self.recordables_data:
            std_tags = self.recordables_data[what].standard_tags

        return NEURONChl_RecGen(src_chl=self, objvar=what, unit_in_nrn=unit_in_nrn, std_tags=std_tags, **kwargs)



NEURONEnvironment.postsynapticmechanisms.register_plugin(NeuroUnitEqnsetPostSynaptic, Neuron_NeuroUnitEqnsetPostSynaptic)
