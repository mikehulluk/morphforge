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
from morphforge.core.misc import FilterExpectSingle, ExpectSingle



class Simulation(object):

    # Syntactic Sugar:
    # ------------------        
    def createCell(self, **kwargs):
        c = self.environment.Cell(simulation=self, **kwargs)
        self.addCell(c)
        return c
    
    def createCurrentClamp(self, **kwargs):
        c = self.environment.CurrentClamp(simulation=self, **kwargs)
        self.addCurrentClamp(c)
        return c

    def createVoltageClamp(self, **kwargs):
        v = self.environment.VoltageClamp(simulation=self, **kwargs)
        self.addVoltageClamp(v)
        return v

    def createSynapse(self, presynaptic_mech, postsynaptic_mech ):
        syn = self.environment.Synapse( simulation = self, presynaptic_mech=presynaptic_mech, postsynaptic_mech=postsynaptic_mech )
        self.addSynapse( syn )
        return syn
    
    def createGapJunction(self, **kwargs):
        gj = self.environment.GapJunction( simulation = self, **kwargs )
        self.addGapJunctionBackendSpecific( gj )
        return gj
    
    
    
    # New API
    def addCurrentClamp(self, cc):
        self.ss_currentClamps.append(cc)
        self.addCurrentClampBackendSpecific(cc)

    def addVoltageClamp(self, cc):
        self.ss_voltageClamps.append(cc)
        self.addVoltageClampBackendSpecific(cc)
    
    def addCell(self, cell):    
        self.ss_cells.append(cell) 
        self.addCellBackendSpecific(cell)
    
    def addSynapse(self, syn):
        self.ss_synapses.append(syn)
        self.addSynapseBackendSpecific( syn )
    
    def addGapJunction(self, gj):
        self.ss_gapjunctions.append(gj)
        self.addGapJunctionBackendSpecific( gj )
        
    
    
    def addCellBackendSpecific(self,cell):
        raise NotImplementedError()    
    def addCurrentClampBackendSpecific(self, vc):
        raise NotImplementedError()
    def addVoltageClampBackendSpecific(self, vc):
        raise NotImplementedError()
    def addSynapseBackendSpecific(self, syn):
        raise NotImplementedError()
    def addGapJunctionBackendSpecific(self, syn):
        raise NotImplementedError()
        
  




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
    def getCells(self):
        return self.ss_cells[:]
    def getVoltageClamps(self):
        return self.ss_voltageClamps[:]
    def getCurrentClamps(self):
        return self.ss_currentClamps[:]
    def getGapJunctions(self):
        return self.ss_gapjunctions[:]
    def getSynapses(self):
        return self.ss_synapses[:]
    
    
    
    

    def Run(self): 
        raise NotImplementedError()
    
    
    
    
    def addRecordable(self, recordable):
        raise NotImplementedError()



    #Syntactic Sugar for making more readable scripts:
    def record( self, recordableSrc, **kwargs):
        recordable = recordableSrc.getRecordable( **kwargs )
        self.addRecordable( recordable )
        return recordable
    
    def recordall( self, membrane_mech, **kwargs):
        for recordable_value in membrane_mech.Recordables.all:
            self.record(membrane_mech, what=recordable_value, description='[%s-%s]'%(membrane_mech.name, recordable_value) ,  **kwargs )







    def getCell(self,cellname=None):
        """ Either return a cell by name if there is more than one cell, otherwise the single cell """
        if cellname:
            return FilterExpectSingle(self.ss_cells, lambda s: s.name==cellname)
        else:
            return ExpectSingle( self.ss_cells)
            
        
        
