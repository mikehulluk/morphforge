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
from biophysics import CellBiophysics

from morphforge.constants import StdRec
from morphforge.core.objectnumberer import ObjectLabeller
from morphforge.core.quantities.fromcore import unit

class Cell(object):
    
    
    
    class Recordables:
        MembraneVoltage = StdRec.MembraneVoltage
    
    

    
    
    def __init__(self,    morphology, simulation, name= None, segmenter=None, initial_voltage=None, cell_tags = [], **kwargs):
        from morphforge.simulation.core.segmentation.cellsegmenter import DefaultCellSegementer
        
        
        

        self.simulation = simulation
        self.name = name if name else ObjectLabeller.getNextUnamedObjectName(Cell, 'AnonCell_')
        self.morphology = morphology 
        
        self.cellSegmenter = segmenter if segmenter else DefaultCellSegementer()
        self.cellSegmenter.connectToCell(self)
        
        
        self.biophysics = CellBiophysics()
    
        self.initial_voltage = initial_voltage or unit("-51:mV")
        
        
        self.cell_tags = cell_tags 
        
        if self.name:
            self.cell_tags = self.cell_tags +  [self.name]
        
        
        
    def getLocation(self, idTag, sectionpos=0.5):
        from celllocation import CellLocation
        return CellLocation(cell=self, section=self.morphology.getSection(idTag=idTag), sectionpos=sectionpos)
    
    def getRegion(self, rgnName):
        return self.morphology.getRegion(rgnName)
    
    def getRegions(self):
        return self.morphology.getRegions()
    
    def getBiophysics(self):        
        return self.biophysics
    
    def getSegmenter(self):
        return self.cellSegmenter

    

