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


from mmcalciumalphabetabeta import MM_CalciumAlphaBetaBetaChannel
from morphforge.core.quantities import unit
from mmwriter_caalphabetabeta import MM_WriterCalciumAlphaBetaBeta
from morphforge.simulation.neuron.hocmodbuilders import MM_ModFileWriterBase
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import MM_Neuron_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable 
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation



class MM_Neuron_CalciumAlphaBetaBeta_Record(NeuronRecordableOnLocation):
    def __init__(self, caAlphaBetaBetaChl, **kwargs):

        super(MM_Neuron_CalciumAlphaBetaBeta_Record,
              self).__init__(**kwargs)
        self.caAlphaBetaBetaChl = caAlphaBetaBetaChl


    def build_mod(self, modfile_set):
        pass

    def buildHocRecVar(self, hocfile_obj, vecname, modvar):
        HocModUtils.create_record_from_modfile(
            hocfile_obj,
            vecname=vecname,
            cell_location=self.cell_location,
            modvariable=modvar,
            mod_neuronsuffix=self.caAlphaBetaBetaChl.get_neuron_suffix(),
            recordobj=self,
            )

    def get_tags(self):
        return []

    def get_description(self):
        return '%s %s' % ('CaValue',
                          self.cell_location.get_location_description_str())



class MM_Neuron_CalciumAlphaBetaBeta_CurrentDensityRecord(MM_Neuron_CalciumAlphaBetaBeta_Record):

    def get_unit(self):
        return unit('mA/cm2')

    def get_std_tags(self):
        return [StandardTags.CurrentDensity]

    def build_hoc(self, hocfile_obj):
        self.buildHocRecVar(hocfile_obj=hocfile_obj, vecname='RecVec%s'
                            % self.name, modvar='i')


class MM_Neuron_CalciumAlphaBetaBeta_RecordState(MM_Neuron_CalciumAlphaBetaBeta_Record):

    def __init__(self, state, **kwargs):
        super(MM_Neuron_CalciumAlphaBetaBeta_RecordState,
              self).__init__(**kwargs)
        self.state = state

    def get_unit(self):
        return unit('1')

    def get_std_tags(self):
        return [StandardTags.StateVariable]

    def build_hoc(self, hocfile_obj):
        self.buildHocRecVar(hocfile_obj=hocfile_obj, vecname='RecVec%s'
                            % self.name, modvar=self.state)

class MM_Neuron_CalciumAlphaBetaBeta_RecordStateVarSteedyState(MM_Neuron_CalciumAlphaBetaBeta_Record):

    def __init__(self, state, **kwargs):
        super(MM_Neuron_CalciumAlphaBetaBeta_RecordStateVarSteedyState,
              self).__init__(**kwargs)
        self.state = state

    def get_unit(self):
        return unit('1')

    def get_std_tags(self):
        return [StandardTags.StateSteddyState]

    def build_hoc(self, hocfile_obj):
        self.buildHocRecVar( hocfile_obj=hocfile_obj, vecname = "RecVec%s"%self.name, modvar=self.state  )



class MM_Neuron_CalciumAlphaBetaBeta_RecordStateVarTimeConstant(MM_Neuron_CalciumAlphaBetaBeta_Record):

    def __init__(self, state, **kwargs):
        super(MM_Neuron_CalciumAlphaBetaBeta_RecordStateVarTimeConstant,
              self).__init__(**kwargs)
        self.state = state

    def get_unit(self):
        return unit('ms')

    def get_std_tags(self):
        return [StandardTags.StateTimeConstant]

    def build_hoc(self, hocfile_obj):
        self.buildHocRecVar(hocfile_obj=hocfile_obj, vecname='RecVec%s'
                            % self.name, modvar=self.state)








class MM_Neuron_CalciumAlphaBetaBeta(MM_CalciumAlphaBetaBetaChannel,
    MM_Neuron_Base):

    def __init__(self, *args, **kwargs):
        MM_CalciumAlphaBetaBetaChannel.__init__(self, *args, **kwargs)
        MM_Neuron_Base.__init__(self)


    def get_recordable(self, what, **kwargs):

        recorders = {
            MM_CalciumAlphaBetaBetaChannel.Recordables.CurrentDensity: MM_Neuron_CalciumAlphaBetaBeta_CurrentDensityRecord,
            MM_CalciumAlphaBetaBetaChannel.Recordables.StateVar: MM_Neuron_CalciumAlphaBetaBeta_RecordState,
            MM_CalciumAlphaBetaBetaChannel.Recordables.StateVarSteadyState: MM_Neuron_CalciumAlphaBetaBeta_RecordStateVarSteedyState,
            MM_CalciumAlphaBetaBetaChannel.Recordables.StateVarTimeConstant: MM_Neuron_CalciumAlphaBetaBeta_RecordStateVarTimeConstant,
            }

        recorder = recorders[what]
        #print recorder
        #print kwargs
        recordable = recorder( caAlphaBetaBetaChl=self,  **kwargs )
        return recordable


    def build_hoc_section( self, cell, section, hocfile_obj, mta ):
        return MM_WriterCalciumAlphaBetaBeta.build_hoc_section( cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta)


    def create_modfile(self, modfile_set):
        MM_WriterCalciumAlphaBetaBeta.build_mod(caAlphaBetaBetaChl=self, modfile_set=modfile_set)


    def get_mod_file_changeables(self):

        change_attrs = set([ 'CaZ', 'name', 'F', 'mechanism_id', 'beta2threshold', 'extracellular_concentration', 'ion', 'R', 'statevars', 'T', 'eqn', 'permeability', 'intracellular_concentration' ])
        #print set( self.__dict__ )
        assert set( self.__dict__) == set( ['mm_neuronNumber', 'cachedNeuronSuffix'] ) | change_attrs

        return dict ( [ (a, getattr(self, a)) for a in change_attrs ] )



# Register the channel
#NeuronSimulationEnvironment.registerMembraneMechanism( MM_CalciumAlphaBetaBetaChannel, MM_Neuron_CalciumAlphaBetaBeta)
NeuronSimulationEnvironment.membranemechanisms.register_plugin( MM_CalciumAlphaBetaBetaChannel, MM_Neuron_CalciumAlphaBetaBeta)
