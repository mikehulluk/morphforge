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

from core import MM_InfTauInterpolatedChannel
from morphforge.units import unit
from mmwriter_infatauinterpolated import NEURONChlWriterInfTauInterpolated
from morphforge.simulation.neuron.hocmodbuilders import MM_ModFileWriterBase
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import NEURONChl_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordable, \
    NEURONRecordableOnLocation


class NEURONChl_InfTauInterpolated_Record(NEURONRecordableOnLocation):

    def __init__(self, alphabeta_chl, modvar, **kwargs):

        super(NEURONChl_InfTauInterpolated_Record,
              self).__init__(**kwargs)
        self.alphabeta_chl = alphabeta_chl
        self.modvar = modvar

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile(
            hocfile_obj,
            vecname='RecVec%s' % self.name,
            cell_location=self.cell_location,
            modvariable=self.modvar,
            mod_neuronsuffix=self.alphabeta_chl.get_neuron_suffix(),
            recordobj=self,
            )


class NEURONChl_InfTauInterpolated_CurrentDensityRecord(NEURONChl_InfTauInterpolated_Record):

    def __init__(self, **kwargs):

        super(NEURONChl_InfTauInterpolated_CurrentDensityRecord,
              self).__init__(modvar='i', **kwargs)

    def get_unit(self):
        return unit('mA/cm2')

    def get_std_tags(self):
        return [StandardTags.CurrentDensity]


class NEURONChl_InfTauInterpolated_ConductanceDensityRecord(NEURONChl_InfTauInterpolated_Record):

    def __init__(self, **kwargs):

        super(NEURONChl_InfTauInterpolated_ConductanceDensityRecord,
              self).__init__(modvar='g', **kwargs)

    def get_unit(self):
        return unit('S/cm2')

    def get_std_tags(self):
        return [StandardTags.ConductanceDensity]


class NEURONChl_InfTauInterpolated_StateVariableRecord(NEURONChl_InfTauInterpolated_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_InfTauInterpolated_StateVariableRecord,
              self).__init__(modvar=state, **kwargs)

    def get_unit(self):
        return unit('')

    def get_std_tags(self):
        return [StandardTags.StateVariable]


class NEURONChl_InfTauInterpolated_StateVariableTauRecord(NEURONChl_InfTauInterpolated_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_InfTauInterpolated_StateVariableTauRecord,
              self).__init__(modvar=state + 'tau', **kwargs)

    def get_unit(self):
        return unit('ms')

    def get_std_tags(self):
        return [StandardTags.StateTimeConstant]


class NEURONChl_InfTauInterpolated_StateVariableInfRecord(NEURONChl_InfTauInterpolated_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_InfTauInterpolated_StateVariableInfRecord,
              self).__init__(modvar=state + 'inf', **kwargs)

    def get_unit(self):
        return unit('')

    def get_std_tags(self):
        return [StandardTags.StateSteadyState]


class NEURONChl_InfTauInterpolated(MM_InfTauInterpolatedChannel, NEURONChl_Base):

    def __init__(self, **kwargs):
        super( NEURONChl_InfTauInterpolated, self).__init__( **kwargs)

    def get_recordable(self, what, **kwargs):

        print 'Getting Reordable', what
        print kwargs

        recorders = {
            MM_InfTauInterpolatedChannel.Recordables.CurrentDensity: NEURONChl_InfTauInterpolated_CurrentDensityRecord,
            MM_InfTauInterpolatedChannel.Recordables.ConductanceDensity: NEURONChl_InfTauInterpolated_ConductanceDensityRecord,
            MM_InfTauInterpolatedChannel.Recordables.StateVar: NEURONChl_InfTauInterpolated_StateVariableRecord,
            MM_InfTauInterpolatedChannel.Recordables.StateVarSteadyState: NEURONChl_InfTauInterpolated_StateVariableInfRecord,
            MM_InfTauInterpolatedChannel.Recordables.StateVarTimeConstant: NEURONChl_InfTauInterpolated_StateVariableTauRecord,
            }
        print 'Getting Reordable', what, recorders[what]
        print kwargs

        return recorders[what](alphabeta_chl=self, **kwargs)


    def build_hoc_section(self, cell, section, hocfile_obj, mta):
        return NEURONChlWriterInfTauInterpolated.build_hoc_section(cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta)

    def create_modfile(self, modfile_set):
        NEURONChlWriterInfTauInterpolated.build_mod(alphabeta_chl=self, modfile_set=modfile_set)

    def get_mod_file_changeables(self):

         # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set(['conductance', 'ion','eqn','conductance','statevars_new','reversalpotential', ])
        assert set(self.__dict__) == set(['_name','_simulation', 'mm_neuronNumber', 'cachedNeuronSuffix']) | change_attrs

        # attrs = ['name','ion','eqn','conductance','statevars_new','reversalpotential',]
        return dict([(a, getattr(self, a)) for a in change_attrs])



# Register the channel
NEURONEnvironment.channels.register_plugin(MM_InfTauInterpolatedChannel, NEURONChl_InfTauInterpolated)
