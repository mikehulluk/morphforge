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


from ..core import StdChlAlphaBetaBeta
from morphforge.core.quantities import unit
from hocmodbuilders.mmwriter_alphabetabeta import NEURONChlWriterAlphaBetaBeta
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import NEURONChl_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordableOnLocation









class NEURONChl_AlphaBetaBeta_Record(NEURONRecordableOnLocation):

    def __init__(self, alphabeta_beta_chl, modvar, **kwargs):
        super(NEURONChl_AlphaBetaBeta_Record, self).__init__(**kwargs)
        self.alphabeta_beta_chl = alphabeta_beta_chl
        self.modvar = modvar

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile(
            hocfile_obj,
            vecname='RecVec%s' % self.name,
            cell_location=self.cell_location,
            modvariable=self.modvar,
            mod_neuronsuffix=self.alphabeta_beta_chl.get_neuron_suffix(),
            recordobj=self,
            )

    def get_description(self):
        return '%s %s %s' % (self.modvar, self.alphabeta_beta_chl.name,
                             self.cell_location.get_location_description_str())


class NEURONChl_AlphaBetaBeta_CurrentDensityRecord(NEURONChl_AlphaBetaBeta_Record):

    def __init__(self, **kwargs):

        super(NEURONChl_AlphaBetaBeta_CurrentDensityRecord,
              self).__init__(modvar='i', **kwargs)

    def get_unit(self):
        return unit('mA/cm2')

    def get_std_tags(self):
        return [StandardTags.CurrentDensity]


class NEURONChl_AlphaBetaBeta_ConductanceDensityRecord(NEURONChl_AlphaBetaBeta_Record):

    def __init__(self, **kwargs):

        super(NEURONChl_AlphaBetaBeta_ConductanceDensityRecord,
              self).__init__(modvar='g', **kwargs)

    def get_unit(self):
        return unit('S/cm2')

    def get_std_tags(self):
        return [StandardTags.ConductanceDensity]


class NEURONChl_AlphaBetaBeta_StateVariableRecord(NEURONChl_AlphaBetaBeta_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_AlphaBetaBeta_StateVariableRecord,
              self).__init__(modvar=state, **kwargs)

    def get_unit(self):
        return unit('')

    def get_std_tags(self):
        return [StandardTags.StateVariable]


class NEURONChl_AlphaBetaBeta_StateVariableTauRecord(NEURONChl_AlphaBetaBeta_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_AlphaBetaBeta_StateVariableTauRecord,
              self).__init__(modvar=state + 'tau', **kwargs)

    def get_unit(self):
        return unit('ms')

    def get_std_tags(self):
        return [StandardTags.StateTimeConstant]


class NEURONChl_AlphaBetaBeta_StateVariableInfRecord(NEURONChl_AlphaBetaBeta_Record):

    def __init__(self, state, **kwargs):

        super(NEURONChl_AlphaBetaBeta_StateVariableInfRecord,
              self).__init__(modvar=state + 'inf', **kwargs)

    def get_unit(self):
        return unit('')

    def get_std_tags(self):
        return [StandardTags.StateSteadyState]


class NEURONChl_AlphaBetaBeta(StdChlAlphaBetaBeta, NEURONChl_Base):

    class Recordables(object):

        CurrentDensity = StandardTags.CurrentDensity


    def __init__(self,  **kwargs):
        super( NEURONChl_AlphaBetaBeta, self).__init__(**kwargs)

    def build_hoc_section(self, cell, section, hocfile_obj, mta):
        return NEURONChlWriterAlphaBetaBeta.build_hoc_section(cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta)

    def create_modfile(self, modfile_set):
        NEURONChlWriterAlphaBetaBeta.build_mod(alphabeta_beta_chl=self, modfile_set=modfile_set)


    def get_recordable(self, what, name, cell_location, **kwargs):

        recorders = {
            StdChlAlphaBetaBeta.Recordables.CurrentDensity: NEURONChl_AlphaBetaBeta_CurrentDensityRecord,
        }

        return recorders[what](alphabeta_beta_chl=self, cell_location= cell_location, name=name, **kwargs )


    def get_mod_file_changeables(self):

         # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set([
            'conductance',
            'beta2threshold',
            'ion',
            'eqn',
            'conductance',
            'statevars',
            'reversalpotential',
            ])
        assert set(self.__dict__) == set(['mm_neuronNumber','_name','_simulation',
                'cachedNeuronSuffix']) | change_attrs

        attrs = [
            'ion',
            'eqn',
            'conductance',
            'statevars',
            'reversalpotential',
            'beta2threshold',
            ]
        return dict([(a, getattr(self, a)) for a in attrs])


# Register the channel
NEURONEnvironment.channels.register_plugin( StdChlAlphaBetaBeta, NEURONChl_AlphaBetaBeta)
