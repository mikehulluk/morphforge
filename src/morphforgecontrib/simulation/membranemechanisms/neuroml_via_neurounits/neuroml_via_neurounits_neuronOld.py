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




from morphforge.simulation.neuron.biophysics.mm_neuron import MM_Neuron_Base
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforgecontrib.simulation.membranemechanisms.common.neuron import  build_hoc_default
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
from neurounits.tools.nmodl import WriteToNMODL
from morphforge.core.quantities.fromcore import unit
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from neurounits.importers.neuroml import EqnSetFromNeuroML








class MM_Neuron_NeuroUnits_GenRecord(NeuronRecordableOnLocation):
    def __init__(self, chl, modvar, **kwargs):
        super( MM_Neuron_NeuroUnits_GenRecord, self).__init__(**kwargs)
        self.chl = chl
        self.modvar=modvar

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile( hocfile_obj,
                                             vecname="RecVec%s"%self.name,
                                             cell_location=self.where,
                                             modvariable=self.modvar,
                                             mod_neuronsuffix=self.chl.nrnsuffix, recordobj=self)

    def get_description(self):
        return "%s %s %s" % (self.modvar, self.chl.name, self.where.get_location_description_str() )


    def get_unit(self):
        return unit("1.0")
    def get_std_tags(self):
        return []



class NeuroML_Via_NeuroUnits_ChannelNEURON(MM_Neuron_Base, NeuroML_Via_NeuroUnits_Channel):

    def __init__(self, xml_filename, chlname=None, mechanism_id=None):
        self.mechanism_id = mechanism_id
        MM_Neuron_Base.__init__(self)
        NeuroML_Via_NeuroUnits_Channel.__init__(self, xml_filename=xml_filename, chlname=chlname, mechanism_id=mechanism_id)




        eqnset,chlinfo,default_params = EqnSetFromNeuroML.load(xml_filename)


        nmodl, buildparameters = WriteToNMODL(eqnset)



        self.defaults = {}
        self.units = {}
        print 'Params:'
        for param_str, value in default_params.iteritems():
            print param_str, value
            sym = eqnset.get_terminal_obj(param_str)
            param_default_unit = buildparameters.symbol_units[sym]

            self.defaults[ param_str] = value.as_quantities_quantity()
            self.units[param_str] = param_default_unit.as_quantities_unit()


        self.modtxt = nmodl
        nrnsuffix = ModFile.extract_nrn_suffix_from_text(self.modtxt)

        self.name = nrnsuffix
        self.nrnsuffix = nrnsuffix

    def build_hoc_section(self, cell, section, hocfile_obj, mta ):
        build_hoc_default( cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta , units=self.units, nrnsuffix=self.nrnsuffix )

    def create_modfile(self, modfile_set):
        modFile =  ModFile(name='NeuroMLViaNeuroUnitsChannelNEURON_%s'%self.name, modtxt=self.modtxt )
        modfile_set.append(modFile)


    def get_variables(self):
        return self.get_defaults().keys()

    def get_defaults(self):
        return self.defaults


    # No Internal recording or adjusting of parameters for now:
    class Recordables:
        all = []

    def get_recordable(self, what,  **kwargs):
        raise ValueError( "Can't find Recordable: %s"%what)







NeuronSimulationEnvironment.membranemechanisms.register_plugin(NeuroML_Via_NeuroUnits_Channel, NeuroML_Via_NeuroUnits_ChannelNEURON)


