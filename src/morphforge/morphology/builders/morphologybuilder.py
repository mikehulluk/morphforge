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

from morphforge.morphology.core import MorphologyTree, Section, Region
from morphforge.core.quantities import  convertToUnit 
import numpy 

class MorphologyBuilder(object):
    """ Class to build simple neuron morphologies """
        
    @classmethod
    def getSingleSectionSoma(cls, rad=None, area=None):
        assert (rad or area) and not(rad and area)
        
        
        if area:
            
            area = convertToUnit(area, defaultUnit="um2" ).rescale("um2").magnitude
            rad = numpy.power((area / (4.0 * numpy.pi)), 1.0 / 2.0)
            
        else:
            assert isinstance(int,rad) or isinstance(float,rad)
            rad = convertToUnit(rad, defaultUnit="um" ).rescale("um").magnitude
            
            
        somaRegion = Region("soma")
        dummysection = Section(region=None, x=0.0, y=0.0, z=0.0, r=rad)
        dummysection.create_distal_section(region=somaRegion, x=rad * 2.0, y=0.0, z=0.0, r=rad, idTag="soma")
        cell = MorphologyTree("SimpleSomaMorph", dummysection=dummysection, metadata={})      
        return cell
    
    
    @classmethod
    def getSomaAxonMorph(cls, axonLength=1000.0, axonRad=0.3, somaRad=20.0, axonSections=10):
        somaRegion = Region("soma")
        axonRegion = Region("axon")
        
        axonSectionLength = float(axonLength) / float(axonSections)
        dummyRoot = Section(region=None, x=0.0, y=0.0, z=0.0, r=somaRad)
        soma = dummyRoot.create_distal_section(region=somaRegion, x=somaRad * 2.0, y=0.0, z=0.0, r=somaRad, idTag="soma")
        prevSection = soma
        for x in range(1, axonSections):
            axon = prevSection.create_distal_section(region=axonRegion, x=x * axonSectionLength + 2.0 * somaRad, y=0, z=0, r=axonRad, idTag="axon_%d" % x)
            prevSection = axon
        cell = MorphologyTree("SimpleSomaAxonMorph", dummysection=dummyRoot, metadata={})
        return cell
        

