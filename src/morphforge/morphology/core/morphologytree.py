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
from morphforge.core import FilterExpectSingle
from morphforge.morphology.visitor import SectionListerDF

    
from section import Section
        
import itertools
from morphologyconsistency import MorphologyConsistencyMgr
from morphforge.morphology.core.morphologybase import MorphologyBase
from morphforge.morphology.conversion import MorphologyConverter


class MorphologyTree(MorphologyBase):
    """
    Class representing a neurons morphology.
    This class contains a link to the base of the tree, a list of regions 
    and a dictionary containing metadata.
    """
    
        
    def to_tree(self):
        return self
    
    def to_array(self, **kwargs):
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
        assert dummysection.isDummySection(), "Dummysection is not a dummy section!"
        
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
    
        
        
 
 
 
        
