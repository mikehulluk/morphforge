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



class AbstCellSegmenter(object):
   
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
    
    
    
                
    
class CellSegmenterStd(AbstCellSegmenter):

    def __init__(self, cell=None, ):
        AbstCellSegmenter.__init__(self, cell)
        self.cellSegments = None        
        
        if self.cell:
            self.connectToCell(cell)

            
    def connectToCell(self, cell):
        assert not self.cell 
        self.cell = cell
        
        
        self.cellSegments = {}
        
        # Segment the cell:
        for section in cell.morphology:
            nSegs = self._getNSegments(section)
            
            self.cellSegments[section] = [ CellSegment(cell=cell, section=section, nsegments=nSegs, segmentno=i, segmenter=self) for i in range(0, nSegs) ] 
    
    def getNumSegments(self, section):
        return len(self.cellSegments[section] )
        
    def getSegments(self, section):
        return self.cellSegments[section]


    def _getNSegments(self, section):
        raise NotImplementedError()

    
    
    
    
    
    
    
    
    
class CellSegmenter_MaxCompartmentLength(CellSegmenterStd):

    def __init__(self, cell=None, maxSegmentLength=5):
        CellSegmenterStd.__init__(self, cell)
        self.maxSegmentLength = maxSegmentLength

    def _getNSegments(self, section):
        return int( section.get_length() / self.maxSegmentLength ) + 1



class CellSegmenter_SingleSegment(CellSegmenterStd):
   
    def _getNSegments(self, section):
        return 1          
           
           
           

class CellSegmenter_MaxLengthByID(CellSegmenterStd):

    def __init__(self, cell=None, section_id_segment_maxsizes=None, defaultSegmentLength=5):
        self.defaultSegmentLength = defaultSegmentLength
        self.section_id_segment_sizes =section_id_segment_maxsizes if section_id_segment_maxsizes is not None else {}

        CellSegmenterStd.__init__(self, cell)

    def _getNSegments(self, section):
        max_size = self.section_id_segment_sizes.get(section.idTag, self.defaultSegmentLength )
        return  int(section.get_length() / max_size )  +1
