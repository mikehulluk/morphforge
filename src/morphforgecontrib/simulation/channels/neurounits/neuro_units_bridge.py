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

from morphforge.simulation.neuron.biophysics.mm_neuron import NEURONChl_Base
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforge.simulation.base.biophysics.channel import Channel
from neurounits.tools.nmodl import WriteToNMODL, MechanismType
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordableOnLocation
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.channels.common.neuron import build_hoc_default
from neurounits.neurounitparser import NeuroUnitParser
from morphforge.core import ObjectLabeller


class RecordableData(object):

    def __init__(self, standard_tags=None):
        self.standard_tags = standard_tags or []


class NEURONChl_RecGen(NEURONRecordableOnLocation):

    def __init__(self, src_chl, modvar, unit_in_nrn, std_tags, **kwargs):
        super(NEURONChl_RecGen, self).__init__(**kwargs)
        self.src_chl = src_chl
        self.modvar = modvar
        self.unit_in_nrn = unit_in_nrn
        self.std_tags = std_tags or []

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile(
            hocfile_obj,
            vecname='RecVec%s' % self.name,
            cell_location=self.cell_location,
            modvariable=self.modvar,
            mod_neuronsuffix=self.src_chl.NRNSUFFIX,
            recordobj=self,
            )

    def get_description(self):
        return '%s %s %s' % (self.modvar, self.src_chl.name,
                             self.cell_location.get_location_description_str())

    def get_unit(self):
        return self.unit_in_nrn

    def get_std_tags(self):
        return self.std_tags





class NeuroUnitEqnsetMechanism(Channel):
    def __init__(self, eqnset,  default_parameters={}, recordables_map= None, recordables_data=None, **kwargs):
        super(NeuroUnitEqnsetMechanism, self).__init__( **kwargs)

        if isinstance(eqnset, basestring):
            eqnset = NeuroUnitParser.EqnSet(eqnset)

        #self.name = name if name is not None else ObjectLabeller.get_next_unamed_object_name(NeuroUnitEqnsetMechanism)
        self._parameters = default_parameters
        self.eqnset = eqnset
        self.recordables_map = recordables_map or {}
        self.recordables_data = recordables_data or {}

        for param in eqnset.parameters:
            print 'CHECKING'
            print param
            print param.symbol
            print 'iii', param.get_dimension().as_quantities_unit(), type(param.get_dimension().as_quantities_unit())
            print "iiii", default_parameters[param.symbol], type(default_parameters[param.symbol])
            assert param.symbol in default_parameters
            assert (param.get_dimension().as_quantities_unit() / default_parameters[param.symbol]).rescale("")
            print 'OK\n'

    def get_defaults(self):
        return self._parameters

    def get_variables(self):
        return self._parameters.keys()



from morphforge.simulationanalysis.summaries_new import SummariserObject
from morphforge.simulationanalysis.summaries_new import SummariserLibrary
from neurounits.writers import MRedocWriterVisitor
import mredoc as mrd

#import mredoc as mrd
class NeuroUnitEqnsetMechanismSummariser(SummariserObject):
    @classmethod
    def build(cls, obj):
        return mrd.HierachyScope(
                MRedocWriterVisitor.build(obj.eqnset)
                )

SummariserLibrary.register_summariser(NeuroUnitEqnsetMechanism, NeuroUnitEqnsetMechanismSummariser)








class Neuron_NeuroUnitEqnsetMechanism(NEURONChl_Base, NeuroUnitEqnsetMechanism):
    def __init__(self, **kwargs):
        super(Neuron_NeuroUnitEqnsetMechanism, self).__init__(**kwargs)

        self.nmodl_txt, self.buildparameters = WriteToNMODL(self.eqnset, neuron_suffix="NRNEQNSET"+ObjectLabeller.get_next_unamed_object_name(Neuron_NeuroUnitEqnsetMechanism, prefix=""))




        assert self.buildparameters.mechanismtype == MechanismType.Distributed
        self.units = {}
        for (param_str, value) in self._parameters.iteritems():
            sym = self.eqnset.get_terminal_obj(param_str)
            param_default_unit = self.buildparameters.symbol_units[sym]
            self.units[param_str] = param_default_unit.as_quantities_unit()

        self.NRNSUFFIX = self.buildparameters.suffix

    def build_hoc_section(self, cell, section, hocfile_obj, mta):
        build_hoc_default(cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta , units=self.units, nrnsuffix=self.buildparameters.suffix)

    def create_modfile(self, modfile_set):
        modfile_set.append(ModFile(name=self.name, modtxt=self.nmodl_txt, strict_modlunit=True))


    def get_mod_file_changeables(self):
        change_attrs = set([ "nmodl_txt", 'recordables_map', 'buildparameters', 'units', 'recordables_data'])
        fixed_attrs = set(['_name','_simulation', 'mm_neuronNumber', 'cachedNeuronSuffix', 'eqnset', '_parameters'])
        print set(self.__dict__)
        assert set(self.__dict__) == fixed_attrs | change_attrs
        return dict([(a, getattr(self, a)) for a in change_attrs])

    def get_recordables(self):
        return self._get_recordable_symbols()
        assert False

    def _get_recordable_symbols(self):
        return [s.symbol for s in list(self.eqnset.states)
                + list(self.eqnset.assignedvalues)
                + list(self.eqnset.suppliedvalues)
                + list(self.eqnset.parameters)]

    def get_recordable(self, what, cell_location, **kwargs):

        # Map it through the recordables_map, so that we can alias to StandardTags:
        what = self.recordables_map.get(what, what)

        valid_symbols = self._get_recordable_symbols()
        if not what in  valid_symbols:
            err ="Unknown record value: %s. Expecting one of: %s "%(what, valid_symbols)
            raise ValueError(err)

        obj = self.eqnset.get_terminal_obj(what)
        unit_in_nrn = self.buildparameters.symbol_units[obj].as_quantities_unit()

        std_tags = []
        if what in self.recordables_data:
            std_tags = self.recordables_data[what].standard_tags

        return NEURONChl_RecGen(src_chl=self, modvar=what, cell_location=cell_location, unit_in_nrn=unit_in_nrn, std_tags=std_tags, **kwargs)



NEURONEnvironment.channels.register_plugin(NeuroUnitEqnsetMechanism, Neuron_NeuroUnitEqnsetMechanism)





