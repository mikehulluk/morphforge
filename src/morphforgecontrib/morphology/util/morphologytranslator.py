#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.morphology.core import Section
from morphforge.morphology.core import Region
from morphforge.morphology.core import MorphologyTree




class MorphologyTranslator(object):


    @classmethod
    def translate(cls, morphology, offset):
        print offset
        #assert False

        #distToParent = SectionVistorFactory.dict_section_proximal_dist_from_soma(morph=morphology, soma_centre=False)()

        sectionMappingTable = {}
        regionMappingTable = {}

        #Create New Regions:
        regionMappingTable[None] = None
        for rOld in morphology.get_regions():
            rNew = Region(name = rOld.name )
            regionMappingTable[rOld] = rNew


        # Create New Sections:
        dummyRootOld = morphology.get_dummy_section()
        dummyRootNew = Section(region=regionMappingTable[dummyRootOld.region], x=dummyRootOld.d_x + offset[0], y=dummyRootOld.d_y+ offset[1], z=dummyRootOld.d_z + offset[2], r=dummyRootOld.d_r)
        sectionMappingTable[dummyRootOld] = dummyRootNew
        for sectionOld in morphology:
            #if distToParent[sectionOld] > max_dist_to_parent: continue

            oldParent = sectionOld.parent
            newParent = sectionMappingTable[ oldParent ]

            sectionNew = newParent.create_distal_section(
                                          region = regionMappingTable[ sectionOld.region ],
                                          x= sectionOld.d_x + offset[0],
                                          y= sectionOld.d_y + offset[1],
                                          z= sectionOld.d_z + offset[2],
                                          r= sectionOld.d_r,
                                          idtag=sectionOld.idtag
                                          )
            sectionMappingTable[sectionOld] = sectionNew

        m = MorphologyTree("translatedNeuron",dummysection = dummyRootNew,metadata={} )
        return m








