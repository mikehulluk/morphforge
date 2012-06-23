#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

from morphforge.core import LocMgr, SettingsMgr
from morphforge.core.misc import SeqUtils



class Simulation(object):

    # Syntactic Sugar:
    # ------------------
    def create_cell(self, **kwargs):
        c = self.environment.Cell(simulation=self, **kwargs)
        self.add_cell(c)
        return c

    def create_currentclamp(self, **kwargs):
        c = self.environment.CurrentClamp(simulation=self, **kwargs)
        self.add_currentclamp(c)
        return c

    def create_voltageclamp(self, **kwargs):
        v = self.environment.VoltageClamp(simulation=self, **kwargs)
        self.add_voltageclamp(v)
        return v

    def create_synapse(self, presynaptic_mech, postsynaptic_mech ):
        syn = self.environment.Synapse( simulation = self, presynaptic_mech=presynaptic_mech, postsynaptic_mech=postsynaptic_mech )
        self.add_synapse( syn )
        return syn

    def create_gapjunction(self, **kwargs):
        gj = self.environment.GapJunction( simulation = self, **kwargs )
        self.add_gapjunction( gj )
        return gj



    # New API
    def add_currentclamp(self, cc):
        self.ss_currentClamps.append(cc)
        self.add_currentclamp_backend_specific(cc)

    def add_voltageclamp(self, cc):
        self.ss_voltageClamps.append(cc)
        self.add_voltageclamp_backend_specific(cc)

    def add_cell(self, cell):
        self.ss_cells.append(cell)
        self.add_cell_backend_specific(cell)

    def add_synapse(self, syn):
        self.ss_synapses.append(syn)
        self.add_synapse_backend_specific( syn )

    def add_gapjunction(self, gj):
        self.ss_gapjunctions.append(gj)
        self.add_gapjunction_backend_specific( gj )



    def add_cell_backend_specific(self,cell):
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
        return set( [ cell.population for cell in self.ss_cells if cell.population])
    @property
    def synapse_populations(self):
        return set( [ syn.population for syn in self.ss_synapses if syn.population])

    @property
    def synapses(self):
        return self.ss_synapses

    @property
    def gapjunctions(self):
        return self.ss_gapjunctions





    def __init__(self, name, environment, **kwargs):
        name = name if name else "Unnamed Simulation"
        self.name = name
        self.environment = environment
        self.simsettings = self.environment.SimulationSettings(**kwargs)
        self.result = None



        # For checksumming: we store links to additional classes:
        self.configClasses = [SettingsMgr, LocMgr]


        # These should only be used by this
        # class, subclasses should take care of the
        # management of cells, VC's and CC's themselves.
        self.ss_cells = []
        self.ss_voltageClamps = []
        self.ss_currentClamps = []

        self.ss_gapjunctions = []
        self.ss_synapses = []



    # For use by summarisers:
    def get_cells(self):
        return self.ss_cells[:]
    def get_voltageclamps(self):
        return self.ss_voltageClamps[:]
    def get_currentclamps(self):
        return self.ss_currentClamps[:]
    def get_gapjunctions(self):
        return self.ss_gapjunctions[:]
    def get_synapses(self):
        return self.ss_synapses[:]





    def run(self):
        raise NotImplementedError()




    def add_recordable(self, recordable):
        raise NotImplementedError()



    #Syntactic Sugar for making more readable scripts:
    def record( self, recordableSrc, **kwargs):
        recordable = recordableSrc.get_recordable( **kwargs )
        self.add_recordable( recordable )
        return recordable

    def recordall( self, membrane_mech, **kwargs):
        for recordable_value in membrane_mech.Recordables.all:
            self.record(membrane_mech, what=recordable_value, description='[%s-%s]'%(membrane_mech.name, recordable_value) ,  **kwargs )

    def get_cell(self,cellname=None):
        """ Either return a cell by name if there is more than one cell, otherwise the single cell """
        if cellname:
            return SeqUtils.filter_expect_single(self.ss_cells, lambda s: s.name==cellname)
        else:
            return SeqUtils.expect_single( self.ss_cells)




