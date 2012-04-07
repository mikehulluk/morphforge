#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
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



"""Tree-based object-model of morphologies.

In the tree based representation, a morphology is considered as a set of
:py:class:`~.Section`. A :py:class:`~.Section` is an unbranching length
neurons, which can be connected to other sections at its end points. If it does
connect to other sections at the end points, then it shares the same position
and radius information at that point.



.. image:: /img_srcs/new_morphology_overview_simplecylinders_tree_simple.svg
    :align: center

For example, Figure 1 shows a morphology composed of 4 sections. Each end of
each frustra is specified as a point in 3D space and a radius:
:math:`(X,Y,Z);R`.  However, since positions and radii are shared, at join
points, only stores a reference to its parent (orange arrow), and its distal
coordinate (red dots).  Therefore 


.. math::

    Section1^{distal}(x,y,z,r)=Section2^{proximal}(x,y,z,r) = (10,0,0,20) 
    
    Section2^{distal}(x,y,z,r)=Section3^{proximal}(x,y,z,r) = (20,0,0,10)
    
    ...

Some care need to be taken around the start of the tree. In order for
`Section1` to have some length, We introduce a special Section, with no parent
(and hence no length), called the Dummy-Section, shown as a blue dot. This
section is just used for its position & radius coordinate; it does not
represent any volume or surface area.

The dummy section is always the root of the tree. Sections whose parents are
the Dummy-Section, are 'Root' sections. (shown in light green).  This means
that there can be many root nodes in a tree, for example:

.. image:: /img_srcs/new_morphology_overview_simplecylinders_tree_complex.svg
    :align: center


.. note::

    There is an assumption that the root nodes in the models are found made 
    at the somata of cells. The terms 'Proxmial' and 'Distal' on Section objects 
    refer to the ends closest and furthest away from the dummyroot section
    respectively.     


.. note::
    
    This object model is heavily based on the .swc file format. DummyNode
    correspond to lines in the .swc format with a parent ID of -1. 


To construct the morphology in the top figure; the code would look like:


.. code-block:: python

    askjdls
    asljf



.. todo::

    This is not the way morphologies are recommended to be built. 
    It may be more convenient to use the 'DictionaryLoader'
    
    


Regions provide a way to group sections together, for example as 'axon',
'soma'.  Each Section in a morphology can optionally be assigned to a single
Region.  Regions are used by the :py:mod:`morphforge.simulation` layer for
specifying channel distributions over a morphology. 

.. note::
    
    This way of specifying Regions is very similar to the 'type' field in the .swc file format.
     
Finally, each Section can be assigned an 'ID-Tag'. This is simply a string that
can be used to refer to a particular section easily later. An IDTag can not be
repeated in a morphology.  For example, when constructing a morphology, we
might tag the main soma section, so that is it simple to add current clamps for
exampl in simulations. 


.. todo::

    Reference some example.    
    
"""







import numpy
import math
import itertools

from morphforge.core import FilterExpectSingle
from morphforge.core import CheckValidName

from morphforge.morphology.core.base import MorphologyBase
from morphforge.morphology.visitor import SectionListerDF
from morphologyconsistency import MorphologyConsistencyMgr




class Section(object):
    d_x = property(lambda self: self._d_pos[0], None, doc="Distal x coordinate")  #coordinate
    d_y = property(lambda self: self._d_pos[1], None, doc="Distal y coordinate")  #coordinate
    d_z = property(lambda self: self._d_pos[2], None, doc="Distal z coordinate")  #coordinate
    d_r = property(lambda self: self._d_r, None, doc="Distal radius")       #radius
    
    p_x = property(lambda self: self.parent._d_pos[0], None, doc="Proximal x coordinate")  #coordinate
    p_y = property(lambda self: self.parent._d_pos[1], None, doc="Proximal y coordinate")  #coordinate
    p_z = property(lambda self: self.parent._d_pos[2], None, doc="Proximal z coordinate")  #coordinate
    p_r = property(lambda self: self.parent._d_r, None, doc="Proximal radius")       #radius

    #  TODO: Make Readonly:
    region = property(lambda self: self._region, None)
    idTag = property(lambda self: self._idTag, None)
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
        if not self.is_dummy_section():
            if not self in self.parent.children:
                self.parent.children.append(self)
        
    def create_distal_section(self, x, y, z, r, region, idTag=None):
        return Section(parent=self, x=x, y=y, z=z, r=r, region=region, idTag=idTag)

    def is_a_root_section(self):
        if self.is_dummy_section(): 
            return False
        return self.parent.is_dummy_section() == True
        
    def is_dummy_section(self):
        return  self.parent == None
    
    def isLeaf(self):
        return len( self.children ) == 0
    
    

    def getNPA4(self, position):
        assert 0 <= position <= 1 
        
        return self.getProximalNPA4() + self.getDistalVectorNP4() * position  
    

    def getDistalNPA3(self):
        """Returns the 3 coordinates of the distal end of the section.  """
        return self._d_pos
    
    def getDistalNPA4(self):
        """Returns the 3 coordinates and the radius of the distal end of the
            section.  """
        return numpy.array((self.d_x, self.d_y, self.d_z, self.d_r))

    def getProximalNPA3(self):
        """ Returns the 3 coordinates of the proximal end of the section.  """
        assert not self.is_dummy_section()
        return self.parent._d_pos
    
    def getProximalNPA4(self):
        """ Returns the 3 coordinates and the radius of the proximal end of the section.  """
        assert not self.is_dummy_section()
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
        assert not self.is_dummy_section(), "Getting Length of dummy section!"
        return numpy.linalg.norm( self.getDistalVectorNP3() )  
    
    
    def getArea(self,include_end_if_terminal=False):
        """ Returns the area of the section.  """
        # http://mathworld.wolfram.com/ConicalFrustum.html
        assert not self.is_dummy_section(), "Getting area of dummy section!"
        
        
        R = self.d_r 
        r = self.p_r
        lateral_area =  math.pi * (R+r) * math.sqrt( (R-r)**2 + self.getLength()**2 )  
        
        if include_end_if_terminal==True and self.isLeaf() :
           return lateral_area + ( math.pi * R**2 ) 
        else:
            return lateral_area
            
        


















class Region(object):
    """
    Region is a collection of sections. It is used for annotating the sections
    (i.e. axon, soma, proximal dendrite, ...) and for collectively assigning 
    the channels and membrane definitions to the sections.
    """    
    
    
    def __str__(self):
        s = "<RegionObject: Name: %s, nSections: %d>" % (self.name, len(self.sections) )
        return s
    def __init__(self, name):
        CheckValidName(name)
        self.name = name
        self.sections = []
        self.morph = None
    
    
    def __iter__(self):
        return iter(self.sections)
    
    def addSection(self, section):
        """Adding a section to the region."""
        
        if section in self.sections: 
            raise ValueError("Section already in Region.sections")

        self.sections.append(section)
        
    
    def setMorph(self, morph):

        if not morph: 
            raise ValueError()
        if self.morph: 
            raise ValueError()
        self.morph = morph






class MorphLocation(object):
    
    # Read-only's:
    @property
    def section(self):
        return self._section
    @property
    def sectionpos(self):
        return self._sectionpos
        

    def __init__(self, section, sectionpos):
        self._section = section
        self._sectionpos = sectionpos
        assert 0.0 <= sectionpos <= 1.0
    
    def getPt3D(self,):
        local_vector = self.sectionpos * self.section.getDistalVectorNP3()
        return self.section.getProximalNPA3() + local_vector










class MorphologyTree(MorphologyBase):
    """
    
    

    
    
    
    """
    
        
    def to_tree(self):
        return self
    
    def to_array(self, **kwargs):
        from morphforge.morphology.conversion import MorphologyConverter
        return MorphologyConverter.tree_to_array(self,**kwargs)
        
    
    
    
    
    
    
    
    def __init__(self, name=None, dummysection=None, metadata=None, region_number_to_name_bidict=None):    
        MorphologyBase.__init__(self, region_number_to_name_bidict=region_number_to_name_bidict, name=name, metadata=metadata)
        
        self._regions = None
        self._dummysection = None
        
        if dummysection:
            self.setDummySection(dummysection)
        
        self.ensureConsistency(requiretreeset=False)
        
    
    
    def __str__(self):
        s = "MorphologyTree Object: Name: %s, nSections: %d, Regions:[%s], idTags:[%s]" % (self.name, 
                                                                       len(self), 
                                                                       ",".join([rgn.name for rgn in self.getRegions()]),
                                                                       ",".join(self.getIDTags())
                                                                       )
        return s
    
    
    # It is not nessesary to define the dummy node when we call __init__,
    # but we need to check it is set before being requested.         
    def isDummySectionSet(self):
        """ Returns whether a tree has been assigned to this morphology"""
        return self._dummysection != None
    
    
    def setDummySection(self, dummysection):
        """ Set the tree node for the morphology. You can only do this to a morphology
        which has not had its tree assigned yet. The root-object of the tree is a 'dummysection',
        but this is **not** the same as a root node.
        """
        assert not self.isDummySectionSet(), "Setting of MorphologyTree Twice"
        assert isinstance(dummysection, Section), "Setting the tree with something that is not a Section object"
        assert dummysection.is_dummy_section(), "Dummysection is not a dummy section!"
        
        assert MorphologyConsistencyMgr.getChecker(self).disable()
        self._dummysection = dummysection
        for r in self.getRegions(): 
            r.setMorph(self)
        assert MorphologyConsistencyMgr.getChecker(self).enable()
        
        assert self.ensureConsistency(), "Morphology is not consistent"
        
        
    
            
            
    def _every_section(self):
        """Includes dummy section"""
        return itertools.chain( *[[self.getDummySection()], self  ] )


    # Iteration over morphologies:
            
    def __iter__(self):
        """ Iteration over each of the sections."""
        
        assert self.ensureConsistency(), "Morphology is not consistent"
        
        #TODO: replace this with a iterator method on one of the sections in the tree. I 
        # need to think about this. it might be the dummysection. This will be cleaner.
        return iter(SectionListerDF(self)())
        
    def __len__(self):
        """Returns the numbers of sections in the morphology """
        assert self.ensureConsistency()
        
        # TODO: as per iter
        return len(SectionListerDF(self)())
    
    
    
    
    
    def getDummySection(self):
        assert self.ensureConsistency(), "MorphologyTree not consistent"
        return self._dummysection
    
    def getRootSection(self):
        assert False, 'Deprecated'
        assert self.ensureConsistency(), "MorphologyTree not consistent"
        return self._dummysection.children[0]
    
    def getRootSections(self):
        return self._dummysection.children
    
    
    
    def getRegions(self):    
        """ Returns a list of unique regions in the morphology
        """
        assert self.ensureConsistency()
        
        if not self._regions:
            allRegions = [ section.region for section in self]
            self._regions = list(set(allRegions))
            if self._regions.__contains__(None): 
                self._regions.remove(None)
        return self._regions
        
    def getRegionNames(self):
        return [ r.name for r in self.getRegions()]
        
    def getRegion(self, name):
        """ Returns a Region object relevant to this tree, given a filename"""
        assert self.ensureConsistency()
        
        return FilterExpectSingle(self.getRegions(), lambda r: r.name == name)
    
    def getSection(self, idTag):
        """ Returns a Section object with a given id"""
        assert self.ensureConsistency()
        return FilterExpectSingle(self, lambda s: s.idTag == idTag)
     
    def getIDTags(self):
        return [ section.idTag for section in self if section.idTag]

    


    def ensureConsistency(self, requiretreeset=True):
        """ 
        This method is used to check the consistency of the tree. In production code, all calls to this should be optimised out using 
        -O optimisation to python.
        This requests a check from MorphologyConsistencyMgr. We do this to avoid storing additional attributes in the MorphologyTree
        Object, which could cause upset for calculating md5sums or pickling.
        """
        if requiretreeset:
            assert self.isDummySectionSet()
        
        
        MorphologyConsistencyMgr.Check(self)
        return True
    
        
        
 
 
 
        

