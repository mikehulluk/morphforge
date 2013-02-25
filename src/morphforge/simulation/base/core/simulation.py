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

from morphforge.core import LocMgr, SettingsMgr
from morphforge.core.misc import SeqUtils

import itertools

class Simulation(object):

    # Syntactic Sugar:
    # ------------------
    def create_cell(self, **kwargs):
        cell = self.environment.Cell(simulation=self, **kwargs)
        self.add_cell(cell)
        return cell

    def create_currentclamp(self, **kwargs):
        current_clamp = self.environment.CurrentClamp(simulation=self, **kwargs)
        self.add_currentclamp(current_clamp)
        return current_clamp

    def create_voltageclamp(self, **kwargs):
        voltage_clamp = self.environment.VoltageClamp(simulation=self, **kwargs)
        self.add_voltageclamp(voltage_clamp)
        return voltage_clamp

    def create_synapse(self, trigger, postsynaptic_mech):
        syn = self.environment.Synapse(simulation=self,
                trigger=trigger,
                postsynaptic_mech=postsynaptic_mech)
        self.add_synapse(syn)
        return syn

    def create_gapjunction(self, **kwargs):
        gap_junction = self.environment.GapJunction(simulation=self, **kwargs)
        self.add_gapjunction(gap_junction)
        return gap_junction

    # New API
    def add_currentclamp(self, cc):
        assert not cc.name in self.objectnames, 'Duplicate name found: %s'%cc.name
        self._current_clamps.append(cc)
        self.add_currentclamp_backend_specific(cc)

    def add_voltageclamp(self, vc):
        assert not vc.name in self.objectnames, 'Duplicate name found: %s'%vc.name
        self._voltage_clamps.append(vc)
        self.add_voltageclamp_backend_specific(vc)

    def add_cell(self, cell):
        assert not cell.name in self.objectnames, 'Duplicate name found: %s'%cell.name
        self._cells.append(cell)
        self.add_cell_backend_specific(cell)

    def add_synapse(self, syn):
        assert not syn.name in self.objectnames, 'Duplicate name found: %s'%syn.name
        self._synapses.append(syn)
        self.add_synapse_backend_specific(syn)

    def add_gapjunction(self, gj):
        assert not gj.name in self.objectnames, 'Duplicate name found: %s'%gj.name
        self._gapjunctions.append(gj)
        self.add_gapjunction_backend_specific(gj)

    def add_recordable(self, recordable):
        assert not recordable.name in self.objectnames, 'Duplicate name found: %s'%recordable.name
        self._recordables.append(recordable)
        self.add_recordable_backend_specific(recordable)

    def add_recordable_backend_specific(self, recordable):
        raise NotImplementedError()

    def add_cell_backend_specific(self, cell):
        raise NotImplementedError()

    def add_currentclamp_backend_specific(self, vc):
        raise NotImplementedError()

    def add_voltageclamp_backend_specific(self, vc):
        raise NotImplementedError()

    def add_synapse_backend_specific(self, syn):
        raise NotImplementedError()

    def add_gapjunction_backend_specific(self, syn):
        raise NotImplementedError()

    @property
    def neuron_populations(self):
        return set([cell.population for cell in self._cells
                   if cell.population])

    @property
    def synapse_populations(self):
        return set([syn.population for syn in self._synapses
                   if syn.population])

    @property
    def are_all_cells_in_pops(self):
        for cell in self._cells:
            if not cell.population:
                return False
        return True




    @property
    def cells(self):
        return self._cells

    @property
    def synapses(self):
        return self._synapses

    @property
    def gapjunctions(self):
        return self._gapjunctions

    @property
    def voltage_clamps(self):
        return self._voltage_clamps
    @property
    def current_clamps(self):
        return self._current_clamps
    @property
    def recordables(self):
        return self._recordables

    @property
    def objects(self):
        return itertools.chain(
                self.cells,
                self.synapses,
                self.gapjunctions,
                self.voltage_clamps,
                self.current_clamps,
                self.recordables)
    @property
    def objectnames(self):
        return [obj.name for obj in self.objects]


    def __init__(self, name, environment, **kwargs):
        name = (name if name else 'Unnamed Simulation')
        self.name = name
        self.environment = environment
        self.simsettings = self.environment.SimulationSettings(**kwargs)
        self.result = None

        # For checksumming: we store links to additional classes:
        self.config_classes = [SettingsMgr, LocMgr]

        # These should only be used by this
        # class, subclasses should take care of the
        # management of cells, VC's and CC's themselves.
        self._cells = []
        self._voltage_clamps = []
        self._current_clamps = []

        self._gapjunctions = []
        self._synapses = []
        self._recordables = []

        # Postprosessing
        self._postprocessors = []


    # Over-ridden in child classes:
    def run(self, **kwargs):
        raise NotImplementedError()

    #def add_recordable(self, recordable):
    #    raise NotImplementedError()

    # Syntactic Sugar for making more readable scripts:
    def record(self, recordable_src=None, **kwargs):

        # Allow 'recordable_src' to be missing. In this case; we expect
        # to be recording from the cell, and that there will be
        # a kwarg['cell_location']:
        if recordable_src is None:
            recordable_src = kwargs['cell_location'].cell

        recordable = recordable_src.get_recordable(simulation=self,
                **kwargs)
        self.add_recordable(recordable)
        return recordable

    def recordall(self, membrane_mech, **kwargs):
        for recordable_value in membrane_mech.Recordables.all:
            self.record(membrane_mech, what=recordable_value,
                        description='[%s-%s]' % (membrane_mech.name,
                        recordable_value), **kwargs)

    def get_cell(self, cellname=None):
        """ Either return a cell by name if there is more than one cell, otherwise the single cell """

        if cellname:
            return SeqUtils.filter_expect_single(self.cells,
                    lambda s: s.name == cellname)
        else:
            return SeqUtils.expect_single(self.cells)


    def get_all_channels(self):
        return list(set(itertools.chain(*[cell.biophysics.get_all_channels_applied_to_cell() for cell in self.cells])) )


    
    def do_result_post_processing(self,):

        for pp in self._postprocessors:
            pp(result=self.result)


    # Post processing:

