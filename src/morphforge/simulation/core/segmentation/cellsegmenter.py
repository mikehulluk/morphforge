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
from morphforge.simulation.core.segmentation.segment import CellSegment



class AbstCellSegementer(object):
   
    def __init__(self, cell=None):
        self.cell = cell
 
    def connectToCell(self, cell):
        raise NotImplementedError()
    
    
    def getNumSegments(self, section):
        raise NotImplementedError()
    
    def getSegments(self, section):
        raise NotImplementedError()

    def __iter__(self):
        for section in self.cell.morphology:
            for seg in self.getSegments(section):
                yield seg
    
    def getNumSegmentTotal(self):
        return sum( [ self.getNumSegments(section) for section in self.cell.morphology] ) 
    
    
    
                
    
class DefaultCellSegementer(AbstCellSegementer):

    def __init__(self, cell=None, maxSegmentLength=5):
        AbstCellSegementer.__init__(self, cell)
        self.maxSegmentLength = maxSegmentLength

        # Initialised when connectToCell is called:
        self.nSegmentMap = None
        self.cellSegments = None        

        
        if self.cell:
            self.connectToCell(cell)
            
    def connectToCell(self, cell):
        assert not self.cell 
        self.cell = cell
        
        self.nSegmentMap = {}
        self.cellSegments = {}
        
        # Segment the cell:
        for section in cell.morphology:
            nSegs = int( section.getLength() / self.maxSegmentLength ) + 1
            self.nSegmentMap[section] = nSegs
            self.cellSegments[section] = [ CellSegment(cell=cell, section=section, nsegments=nSegs, segmentno=i, segmenter=self) for i in range(0, nSegs) ] 
    
    def getNumSegments(self, section):
        return self.nSegmentMap[section]
        
    def getSegments(self, section):
        return self.cellSegments[section]
           
           
           
           
           

class IDBasedCellSegementer(AbstCellSegementer):

    def __init__(self, cell=None, section_id_segment_sizes=None, defaultSegmentLength=5):
        AbstCellSegementer.__init__(self, cell)
        
        self.defaultSegmentLength = defaultSegmentLength
        self.section_id_segment_sizes =section_id_segment_sizes if section_id_segment_sizes is not None else {}

        # Initialised when connectToCell is called:
        self.nSegmentMap = None
        self.cellSegments = None        

        if self.cell:
            self.connectToCell(cell)
            
    def connectToCell(self, cell):
        assert not self.cell 
        self.cell = cell
        
        self.nSegmentMap = {}
        self.cellSegments = {}
        
        # Segment the cell:
        for section in cell.morphology:
            sectSize = self.section_id_segment_sizes.get(section.idTag, self.defaultSegmentLength )
            
            nSegs = int( section.getLength() / sectSize ) + 1
            
            self.nSegmentMap[section] = nSegs
            self.cellSegments[section] = [ CellSegment(cell=cell, section=section, nsegments=nSegs, segmentno=i, segmenter=self) for i in range(0, nSegs) ]
             
    
    def getNumSegments(self, section):
        return self.nSegmentMap[section]
        
    def getSegments(self, section):
        return self.cellSegments[section]
