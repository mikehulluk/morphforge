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
#from morphforge.morphology.md5 import _get_md5_of_morphology
#from morphforge.core import getStringMD5Checksum
from morphforge.core.misc import StrUtils

def _get_md5_of_region(r):
    #assert False # Is this Cruft?? Added Jan 2011
    return StrUtils.get_hash_md5(r.name)

def _get_md5_of_section(s):
    #assert False # Is this Cruft?? Added Jan 2011
    section_string = " %2.2f %2.2f %2.2f %2.2f "
    regions_string = _get_md5_of_region(s.region) if s.region else ""
    children_string = ",".join( [_get_md5_of_section(s) for s in s.children] )
    id_string = "" if not s.idtag else StrUtils.get_hash_md5(s.idtag)

    return StrUtils.get_hash_md5( section_string + regions_string + children_string + id_string)


def _get_md5_of_morphology(m):
    #assert False # Is this Cruft?? Added Jan 2011
    treemd5 = _get_md5_of_section(m._dummysection)
    name_md5 = StrUtils.get_hash_md5(m.name)
    assert not m.metadata
    regions_md5 = ",".join( [ _get_md5_of_region(r) for r in m.get_regions() ])
    return StrUtils.get_hash_md5(treemd5 + name_md5 + regions_md5)


class MorphologyConsistencyMgr(object):
    morphologyConsistencyCheckers = {}

    @classmethod
    def check_morphology(cls, morph):
        #return
        return cls.get_checker(morph).run_checks()


    @classmethod
    def get_checker(cls, morph):
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



    def run_checks(self):
        if self.enableStack > 0 :
            #print "Already Checking"
            return

        if self.enableStack != 0:
            return


        # Disable further checking:
        self.disable()

        check_cstyle_varname(self.morph.name)
        self.check_tree()

        # Enable further checking:
        self.enable()


    def check_section(self, section, morph, dummysection=False, recurse=True):
        if dummysection:
            assert section.is_dummy_section()
        else:
            assert not section.is_dummy_section()

        self.check_section_infra_structure(section=section, morph=morph,dummysection=dummysection)
        self.check_section_contents(section=section, morph=morph,dummysection=dummysection)

        if recurse:
            for c in section.children:
                self.check_section(c, morph=morph, dummysection=False, recurse=recurse)


    def check_section_infra_structure(self,section, morph, dummysection):
        from tree import Section
        assert isinstance( self.morph._dummysection, Section)

        # Check the parent/children connections:
        if dummysection:
            self.check_dummy_section(section)
            assert section.is_dummy_section()
            #assert len(section.children)==1
        else:
            assert not section.is_dummy_section()
            assert section in section.parent.children

        # Check the regions are in the morphology list:
        if section.region:
            assert section.region in morph.get_regions()
            assert section in section.region.sections

    def check_dummy_section(self, dummysection):
        assert dummysection.is_dummy_section()
        assert dummysection.parent == None
        assert dummysection.region == None




    def check_section_contents(self, section, morph,dummysection):
        # Check the Radii:
        if not section.is_leaf():

            if section.d_r < 0.0001:
                assert False, 'Very thin distal segment diameter: %f'%section.d_r

        # TODO: Check the radius of the near end of the dummysection segment.


    def check_region(self,region,morph):

        check_cstyle_varname(region.name)
        # Check no-other region has this name:
        #print "Checking region:", region.name
        #print "All Regions:", ",".join( [r.name for r in self.morph.get_regions()] )
        assert SeqUtils.filter_expect_single( self.morph.get_regions(), lambda rgn: rgn.name == region.name) == region
        assert region.morph == morph
        for s in region.sections:
            assert region == s.region


    def check_tree(self):
        if not self.morph.is_dummy_section_set(): return

        dummy_section =  self.morph.get_dummy_section()
        self.check_dummy_section(dummy_section)


        # Check nothing changed in the tree:
        morphmd5 = _get_md5_of_morphology(self.morph)
        if self.morphmd5cache:
            if morphmd5 != self.morphmd5cache:
                raise Exception("MD5 of tree has changed!")
            else:
                return
        self.morphmd5cache = morphmd5

        # Check the tree is sensible:
        self.check_section(self.morph._dummysection, self.morph, dummysection=True, recurse=True)

        # Check that there are not duplications of idTags in the tree:
        idtags = SeqUtils.flatten( [s.idtag for s in self.morph if s.idtag]  )
        #print idtags
        assert len(idtags) == len( list(set(idtags) ) )

        # Check the regions
        for rgn in self.morph.get_regions():
            self.check_region(rgn, self.morph)


