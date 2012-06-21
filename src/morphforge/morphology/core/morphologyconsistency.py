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
from morphforge.core import  SeqUtils,  check_cstyle_varname
#from section import Section        
from morphforge.morphology.md5 import getMD5OfMorphology



class MorphologyConsistencyMgr(object):
    morphologyConsistencyCheckers = {}
    
    @classmethod
    def Check(cls, morph):
        #return
        return cls.getChecker(morph).Check()
    
    
    @classmethod
    def getChecker(cls, morph):
        if not morph in cls.morphologyConsistencyCheckers:
            cls.morphologyConsistencyCheckers[morph] = MorphConsistencyChecker(morph)
        return cls.morphologyConsistencyCheckers[morph]




class MorphConsistencyChecker(object):
    
        
    
    def __init__(self, morph):
        from morphforge.morphology.core import MorphologyTree
        assert isinstance( morph, MorphologyTree)
        self.morph = morph
        self.morphmd5cache = None

        # If this is enabled, then enableStack will be 0.
        # We do this to prevent checking of the morph during
        # its construction
        self.enableStack=0        
        
    def disable(self):
        self.enableStack += 1
        return True
    
    def enable(self):
        self.enableStack -= 1
        assert self.enableStack >= 0
        return True
        
    
    
    def Check(self):
        if self.enableStack > 0 :
            #print "Already Checking" 
            return 
        
        if self.enableStack != 0: 
            return
        
        
        # Disable further checking:
        self.disable()
        
        check_cstyle_varname(self.morph.name)
        self.CheckTree()
    
        # Enable further checking:
        self.enable()
    
    
    def CheckSection(self, section, morph, dummysection=False, recurse=True):
        if dummysection:
            assert section.is_dummy_section()
        else:
            assert not section.is_dummy_section()

        self.CheckSectionInfraStructure(section=section, morph=morph,dummysection=dummysection)
        self.CheckSectionContents(section=section, morph=morph,dummysection=dummysection)
        
        if recurse:
            for c in section.children:
                self.CheckSection(c, morph=morph, dummysection=False, recurse=recurse) 
        
        
    def CheckSectionInfraStructure(self,section, morph, dummysection):
        from tree import Section
        assert isinstance( self.morph._dummysection, Section)
        
        # Check the parent/children connections:
        if dummysection:
            self.CheckDummySection(section)
            assert section.is_dummy_section()
            #assert len(section.children)==1
        else:
            assert not section.is_dummy_section()
            assert section in section.parent.children
        
        # Check the regions are in the morphology list:
        if section.region:
            assert section.region in morph.getRegions()
            assert section in section.region.sections
   
    def CheckDummySection(self, dummysection):
        assert dummysection.is_dummy_section() 
        assert dummysection.parent == None
        assert dummysection.region == None 

      
        
        
    def CheckSectionContents(self, section, morph,dummysection):
        # Check the Radii:
        if not section.is_leaf():
            
            if section.d_r < 0.0001:
                assert False, 'Very thin distal segment diameter: %f'%section.d_r
    
        # TODO: Check the radius of the near end of the dummysection segment.
        
            
    def CheckRegion(self,region,morph):
        
        check_cstyle_varname(region.name)
        # Check no-other region has this name:
        #print "Checking region:", region.name
        #print "All Regions:", ",".join( [r.name for r in self.morph.getRegions()] )
        assert SeqUtils.filter_expect_single( self.morph.getRegions(), lambda rgn: rgn.name == region.name) == region
        assert region.morph == morph
        for s in region.sections:
            assert region == s.region
        
        
    def CheckTree(self):
        if not self.morph.isDummySectionSet(): return

        dummySection =  self.morph.getDummySection()
        self.CheckDummySection(dummySection)        

        
        # Check nothing changed in the tree:
        morphmd5 = getMD5OfMorphology(self.morph)
        if self.morphmd5cache:
            if morphmd5 != self.morphmd5cache:
                raise Exception("MD5 of tree has changed!")
            else:
                return
        self.morphmd5cache = morphmd5
        
        # Check the tree is sensible:
        self.CheckSection(self.morph._dummysection, self.morph, dummysection=True, recurse=True)
        
        # Check that there are not duplications of idTags in the tree:
        idtags = SeqUtils.flatten( [s.idTag for s in self.morph if s.idTag]  )
        #print idtags
        assert len(idtags) == len( list(set(idtags) ) )
        
        # Check the regions
        for rgn in self.morph.getRegions():
            self.CheckRegion(rgn, self.morph)
        

