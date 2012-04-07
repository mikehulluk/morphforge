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
class CellSegment(object):
    def __init__(self, cell, section, nsegments, segmentno, segmenter):
        self.cell = cell
        self.section = section
        self.nsegments = nsegments
        self.segmentno = segmentno
        
        self.segmenter = segmenter
        
    def getSectionPos(self, pSegment):
        # Converts a position from [0-1] within a segment into a 
        # position [0-1] within a section 
        segmentSize = 1.0/self.nsegments
        segmentPosProx = segmentSize * self.segmentno
        sectionpos = segmentPosProx + pSegment * segmentSize
        
        assert 0 <= sectionpos <= 1.0
        return sectionpos
     
    def getCellLocation(self, pSegment=0.5):
        from morphforge.simulation.core.celllocation import CellLocation
        sectionpos = self.getSectionPos(0.5)
        return CellLocation(cell=self.cell, section=self.section, sectionpos=sectionpos)
        
    
        
    def getProximalNP4A(self):
        return self.section.get_npa4( self.getSectionPos(0.0) )
        
    def getDistalNP4A(self):
        return self.section.get_npa4( self.getSectionPos(1.0) )
        
    def getDistanceFromProximalSectionEnd(self, pSegment=0.5):
        return self.getSectionPos(pSegment) * self.section.get_length()
    
    
    
    
    def getParentSegment(self):
        if self.segmentno == 0:
            if self.section.is_a_root_section():
                assert False, 'Need to check here!'
                return None
            else:
                return self.segmenter.getSegments(self.section.parent)[-1]
            
        else:
            return self.segmenter.getSegments(self.section)[self.segmentno-1]
    
