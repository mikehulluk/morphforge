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
from morphforge.morphology.visitor.visitorbaseclasses import  DictBuilderSectionVisitorHomo, NumpyBuilderSectionVisitor
from morphforge.morphology.visitor import SectionVisitorDF

import numpy
import numpy as np 
from morphforge.morphology.visitor.visitorbaseclasses import SectionIndexerDF




class SectionVistorFactory(object):
    
    @classmethod
    def getBoundingBox(cls, morph=None):
        pts = SectionVistorFactory.Array3AllPoints(morph)()
        return (np.min(pts[:,0]), np.max(pts[:,0])) , (np.min(pts[:,1]), np.max(pts[:,1])), (np.min(pts[:,2]), np.max(pts[:,2]))
    
    
    @classmethod
    def Array4AllPoints(cls, morph=None):
        xyzr = []
        def functorRoot(s):
            xyzr.append( s.getProximalNPA4() )
            xyzr.append( s.getDistalNPA4() )
        def functor(s):
            xyzr.append( s.getDistalNPA4() )
        return SectionVisitorDF(functor=functor , morph=morph,rootsectionfunctor=functorRoot, returnfunctor=lambda : np.array(xyzr) )
    
    @classmethod
    def Array3AllPoints(cls, morph=None):
        xyz = []
        def functorRoot(s):
            xyz.append( s.getProximalNPA3() )
            xyz.append( s.getDistalNPA3() )
        def functor(s):
            xyz.append( s.getDistalNPA3() )
        return SectionVisitorDF(functor=functor , morph=morph,rootsectionfunctor=functorRoot, returnfunctor=lambda : np.array(xyz) )
    

    
    
    @classmethod
    def Array3FarPoint(cls, morph=None):
        functor = lambda s: s.getDistalNPA3()
        return NumpyBuilderSectionVisitor(functor=functor, morph=morph, ndims=3, datatype=float)

    @classmethod
    def Array4FarPoint(cls, morph=None):
        functor = lambda s: s.getDistalNPA4()
        return NumpyBuilderSectionVisitor(functor=functor, morph=morph, ndims=4, datatype=float)
    
    
    @classmethod
    def DictSectionLength(cls, morph=None):
        return DictBuilderSectionVisitorHomo(functor=lambda s: s.getLength(), morph=morph)
    
    @classmethod
    def DictSectionRadius(cls, morph=None):
        return DictBuilderSectionVisitorHomo(functor=lambda s:s.d_r, morph=morph)
    
    
    
    @classmethod
    def DictSectionProximalDistFromSoma(cls, morph=None, somaCentre=False):
        assert not somaCentre

        
        

        def DictSectionProximalDistFromSoma(s):
            if s.isDummySection():
                assert False
                
            if s.isARootSection():
                return 0.0
            else:
                #ml2 = MorphLocation(section=s, sectionpos=1.0)
                
                #return MorphPathSimple(ml1, ml2).getLength()
                #print 'Parent Length:', s.parent.getLength()
                d1 = DictSectionProximalDistFromSoma(s.parent) 
                d2 = s.parent.getLength()
                d = d1 + d2
                #print d, d1, d2
                #print s.p_x, s.p_y, s.p_z
                #assert False
                return d
            
            
        return DictBuilderSectionVisitorHomo(functor=DictSectionProximalDistFromSoma, morph=morph)
    
    
    
    @classmethod
    def DictSectionDistalDistFromSoma(cls, morph=None, somaCentre=False):
        assert not somaCentre

        def DictSectionDistalDistFromSoma(s):
            if s.isARootSection():
                return s.getLength()
            else:
                return DictSectionDistalDistFromSoma(s.parent) + s.getLength()
            
        return DictBuilderSectionVisitorHomo(functor=DictSectionDistalDistFromSoma, morph=morph)
    
    
    
    
    
    
    @classmethod
    def DictSectionSA(self,morph=None):
        return DictBuilderSectionVisitorHomo(functor=lambda s: s.getLength() * numpy.pi * s.d_r * 2.0    , morph=morph)
    
    
    
    
        
        
        
    @classmethod
    def getVerticesAndEdges(cls, morph):
        
        sI = SectionIndexerDF(offset=1)
        xyzr = []
        edges = []
        def functorRoot(s):
            xyzr.append( s.getProximalNPA4() )
            xyzr.append( s.getDistalNPA4() )
            edges.append( (0,1) )
        def functor(s):
            xyzr.append( s.getDistalNPA4() )
            edges.append( (sI[s], sI[s.parent]) )
        return SectionVisitorDF(functor=functor , morph=morph, rootsectionfunctor=functorRoot, returnfunctor=lambda : (np.array(xyzr), np.array(edges)) )
      
      
    @classmethod  
    def getSectionIndexer(cls, **kwargs):
        return SectionIndexerDF(**kwargs)
        
        
SVVisitorFactory = SectionVistorFactory






  
    
