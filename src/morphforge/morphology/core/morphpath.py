#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
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

class MorphPathSimple(object):
    def __init__(self, morphloc1, morphloc2):
        self.morphloc1 = morphloc1
        self.morphloc2 = morphloc2
        
         
        # Check Morphlocation1 is upstream of MorphLocation2,
        # and build a list of connecting regions:
        self._connecting_sections = []
        if morphloc1.section != morphloc2.section:
            current_section = self.morphloc2.section.parent
            while current_section != self.morphloc1.section:
                self._connecting_sections.append( current_section )
                assert not current_section.isARootSection()
        
         
        assert not self.morphloc1.section in self._connecting_sections
        assert not self.morphloc2.section in self._connecting_sections
        
         
    def getLength(self):
        s1Length =  (1,-self.morphloc1.sectionpos)* self.morphloc1.section.getLength()
        s2Length =  self.morphloc2.sectionpos * self.morphloc2.section.getLength()    
        connecting_section_lengths = [ s.getLength() for s in self._connecting_sections]
        return s1Length + s2Length + sum(connecting_section_lengths)
    
        
        
    def isSectionInPath(self, section):
        return section in self._connecting_sections
    
    def isSectionOnEndpoint(self, section):
        return section in ( self.morphloc1.section, self.morphloc2.section )
    
