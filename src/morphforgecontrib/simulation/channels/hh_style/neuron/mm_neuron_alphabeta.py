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




from ..core import StdChlAlphaBeta
from morphforge.units import qty, parse_unit_str
from morphforge import units
from hocmodbuilders.mmwriter_alphabeta import NEURONChlWriterAlphaBeta
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import NEURONChl_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordableOnLocation




class NEURONChl_AlphaBeta_Record(NEURONRecordableOnLocation):
    def __init__(self, alphabeta_chl, modvar, **kwargs):
        super(NEURONChl_AlphaBeta_Record, self).__init__(**kwargs)
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

    def get_description(self):
        return '%s %s %s' % (self.modvar, self.alphabeta_chl.name,
                             self.cell_location.get_location_description_str())


class NEURONChl_AlphaBeta_CurrentDensityRecord(NEURONChl_AlphaBeta_Record):

    def __init__(self, **kwargs):
        super(NEURONChl_AlphaBeta_CurrentDensityRecord,
              self).__init__(modvar='i', **kwargs)

    def get_unit(self):
        return parse_unit_str('mA/cm2')

    def get_std_tags(self):
        return [StandardTags.CurrentDensity]


class NEURONChl_AlphaBeta_ConductanceDensityRecord(NEURONChl_AlphaBeta_Record):

    def __init__(self, **kwargs):

        super(NEURONChl_AlphaBeta_ConductanceDensityRecord,
              self).__init__(modvar='g', **kwargs)

    def get_unit(self):
        return parse_unit_str('S/cm2')

    def get_std_tags(self):
        return [StandardTags.ConductanceDensity]


class NEURONChl_AlphaBeta_StateVariableRecord(NEURONChl_AlphaBeta_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_AlphaBeta_StateVariableRecord,
              self).__init__(modvar=state, **kwargs)
        assert state in self.alphabeta_chl.statevars

    def get_unit(self):
        return units.dimensionless

    def get_std_tags(self):
        return [StandardTags.StateVariable]


class NEURONChl_AlphaBeta_StateVariableTauRecord(NEURONChl_AlphaBeta_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_AlphaBeta_StateVariableTauRecord,
              self).__init__(modvar=state + 'tau', **kwargs)
        assert state in self.alphabeta_chl.statevars

    def get_unit(self):
        return parse_unit_str('ms')

    def get_std_tags(self):
        return [StandardTags.StateTimeConstant]


class NEURONChl_AlphaBeta_StateVariableInfRecord(NEURONChl_AlphaBeta_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_AlphaBeta_StateVariableInfRecord,
              self).__init__(modvar=state + 'inf', **kwargs)
        assert state in self.alphabeta_chl.statevars

    def get_unit(self):
        return parse_unit_str('')

    def get_std_tags(self):
        return [StandardTags.StateSteadyState]


class NEURONChl_AlphaBeta(StdChlAlphaBeta, NEURONChl_Base):

    def __init__(self, **kwargs):
        super(NEURONChl_AlphaBeta,self).__init__(**kwargs)

    def get_recordable(self, what, **kwargs):

        # Allow what to be a state-variable, but we need to remap it internally:
        if what in self.statevars.keys():
            assert not 'state' in kwargs
            kwargs['state'] = what
            what = StdChlAlphaBeta.Recordables.StateVar

        recorders = {
            StdChlAlphaBeta.Recordables.CurrentDensity: NEURONChl_AlphaBeta_CurrentDensityRecord,
            StdChlAlphaBeta.Recordables.ConductanceDensity: NEURONChl_AlphaBeta_ConductanceDensityRecord,
            StdChlAlphaBeta.Recordables.StateVar: NEURONChl_AlphaBeta_StateVariableRecord,
            StdChlAlphaBeta.Recordables.StateVarSteadyState: NEURONChl_AlphaBeta_StateVariableInfRecord,
            StdChlAlphaBeta.Recordables.StateVarTimeConstant: NEURONChl_AlphaBeta_StateVariableTauRecord,
            }

        return recorders[what](alphabeta_chl=self, **kwargs)


    def build_hoc_section(self, cell, section, hocfile_obj, mta):
        return NEURONChlWriterAlphaBeta.build_hoc_section(cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta)

    def create_modfile(self, modfile_set):
        NEURONChlWriterAlphaBeta.build_mod(alphabeta_chl=self,
                modfile_set=modfile_set)

    def get_mod_file_changeables(self):

        # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set([ 'ion','eqn','conductance','statevars','reversalpotential',])
        assert set(self.__dict__) == set(['_name','_simulation', 'mm_neuronNumber','cachedNeuronSuffix']) | change_attrs


        return dict([(a, getattr(self, a)) for a in change_attrs])


# Register the channel
NEURONEnvironment.channels.register_plugin(
        StdChlAlphaBeta,
        NEURONChl_AlphaBeta)
