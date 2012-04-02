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

import numpy
import math

class Section(object):
    d_x = property(lambda self: self._d_pos[0], None)  #coordinate
    d_y = property(lambda self: self._d_pos[1], None)  #coordinate
    d_z = property(lambda self: self._d_pos[2], None)  #coordinate
    d_r = property(lambda self: self._d_r, None)       #radius
    
    p_x = property(lambda self: self.parent._d_pos[0], None)  #coordinate
    p_y = property(lambda self: self.parent._d_pos[1], None)  #coordinate
    p_z = property(lambda self: self.parent._d_pos[2], None)  #coordinate
    p_r = property(lambda self: self.parent._d_r, None)       #radius

    def setRegion(self, region):
        assert False, 'Deprecated as of 15-Sept-2011'
        self._region = region

    def setIDTag(self, idTag):
        assert False, 'Deprecated as of 15-Sept-2011'
        assert not self._idTag
        self._idTag = idTag
       
    #  TODO: Make Readonly:
    region = property(lambda self: self._region, setRegion)
    idTag = property(lambda self: self._idTag, setIDTag)
    parent = property(lambda self: self._parent, None)
    children = property(lambda self: self._children, None)
    

    
    def __init__(self, x, y, z, r, region, parent=None, idTag=None):
        """ Creation of the section.  """

        self._d_pos = numpy.array((float(x), float(y), float(z)))
        self._d_r = float(r)
        
        self._parent = parent
        self._children = []
        self._region = region
        self._idTag = idTag
        
        
        # Post Processing: tidy up loose ends:
        if region:
            region.addSection(self)
        if not self.isDummySection():
            if not self in self.parent.children:
                self.parent.children.append(self)
        
    def extrudeChildSection(self, x, y, z, r, region, idTag=None):
        return Section(parent=self, x=x, y=y, z=z, r=r, region=region, idTag=idTag)

    def isARootSection(self):
        if self.isDummySection(): 
            return False
        return self.parent.isDummySection() == True
        
    def isDummySection(self):
        return  self.parent == None
    
    def isLeaf(self):
        return len( self.children ) == 0
    
    

    def getNPA4(self, position):
        assert 0 <= position <= 1 
        
        return self.getProximalNPA4() + self.getDistalVectorNP4() * position  
    

    def getDistalNPA3(self):
        """ Returns the 3 coordinates of the distal end of the section.  """
        return self._d_pos
    
    def getDistalNPA4(self):
        """ Returns the 3 coordinates and the radius of the distal end of the
            section.  """
        return numpy.array((self.d_x, self.d_y, self.d_z, self.d_r))

    def getProximalNPA3(self):
        """ Returns the 3 coordinates of the proximal end of the section.  """
        assert not self.isDummySection()
        return self.parent._d_pos
    
    def getProximalNPA4(self):
        """ Returns the 3 coordinates and the radius of the proximal end of the section.  """
        assert not self.isDummySection()
        return numpy.array((self.p_x, self.p_y, self.p_z, self.p_r))






    def __repr__(self):
        def EndSummary(e): return "[%f,%f,%f, r=%f]" % (e.d_x, e.d_y, e.d_z, e.d_r)
        endString = "SectionObject: " + EndSummary(self.parent) + " -> " + EndSummary(self) + ", "
        rgString = "Region:" + self.region.name +", " if self.region else ""
        idString = "idTag:" + self.idTag + ", " if self.idTag else ""
        lnString = "Length: %2.2f, " % self.getLength()
        return "<" +endString + lnString + rgString + idString +">" 
    


    def getDistalVectorNP3(self):
        """ Returns the vector that joins the proximal end of the section to the distal end.  """
        return self.getDistalNPA3() - self.getProximalNPA3()
    
    def getDistalVectorNP4(self):
        """ Returns the vector that joins the proximal end of the section to the distal end.  """
        return self.getDistalNPA4() - self.getProximalNPA4()
    
    def getVectorfromParentNP4(self):
        """ Returns the directional vector and the radious difference in the section.  """
        return self.getDistalNPA4() - self.getProximalNPA4()
    

    def getLength(self):
        assert not self.isDummySection(), "Getting Length of dummy section!"
        return numpy.linalg.norm( self.getDistalVectorNP3() )  
    
    
    def getArea(self,include_end_if_terminal=False):
        """ Returns the area of the section.  """
        # http://mathworld.wolfram.com/ConicalFrustum.html
        assert not self.isDummySection(), "Getting area of dummy section!"
        
        
        R = self.d_r 
        r = self.p_r
        lateral_area =  math.pi * (R+r) * math.sqrt( (R-r)**2 + self.getLength() )  
        
        if include_end_if_terminal==True and self.isLeaf() :
           return lateral_area + ( math.pi * R**2 ) 
        else:
            return lateral_area
            
        
