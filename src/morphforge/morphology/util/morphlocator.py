#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
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
from morphforge.morphology.visitor.visitorfactory import SectionVistorFactory
from morphforge.morphology.core import MorphLocation
import itertools


class MorphLocator(object):
    
    @classmethod
    def getLocationsAtDistanceAwayFromSoma(cls, morphology, distance, section_predicate=None):
        
        distToSectionDistal = SectionVistorFactory.DictSectionDistalDistFromSoma(morph=morphology, somaCentre=False)()
        
        
        # Section predicates: allows us to generate only on a path, region, etc
        section_predicate = section_predicate if section_predicate else lambda s:True
        
        locations = []
        
        for section in morphology:
            if not section_predicate(section):
                continue
                
                
            if section.isARootSection():
                
                if distance < distToSectionDistal[section]:
                    #assert False, 'Not implemented'
                    locations.append( MorphLocation( section = section, sectionpos = distance/distToSectionDistal[section] )  )
                
                else:
                    
                    pass
                
            else: 
                proximal_dist = distToSectionDistal[section.parent]
                distal_dist = distToSectionDistal[section]
                
                
                # Does a distance fall on this section:
                if proximal_dist < distance < distal_dist:
                    prop = (distance - proximal_dist) / ( distal_dist - proximal_dist)
                    assert 0.0 <= prop <= 1.0
                    locations.append( MorphLocation( section=section, sectionpos=prop) )
                else:
                    pass
            
            
        #print 'Distance', distance, len(locations) 
        #assert len( locations ) == 1       
        return locations
        
        
        
        
    @classmethod
    def getLocationsAtDistancesAwayFromSoma(cls, morphology, distances, section_predicate=None):
        return list( itertools.chain( *[cls.getLocationsAtDistanceAwayFromSoma(morphology, distance, section_predicate=section_predicate) for distance in distances]  ) )
        
        
