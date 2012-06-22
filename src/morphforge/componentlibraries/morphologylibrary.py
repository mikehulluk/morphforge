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
class MorphologyLibrary(object):
    
    morphFuncs = dict()
    
    
    @classmethod
    def register_morphology(cls, modelsrc, celltype , morphFunctor):
        key = modelsrc, celltype
        assert not key in cls.morphFuncs
        cls.morphFuncs[ key ] = morphFunctor
        
        
        
    @classmethod        
    def get_morphology_functor(cls, celltype, modelsrc=None ):
        return cls.morphFuncs [ (modelsrc, celltype) ]
    
    @classmethod        
    def get_morphology(cls, celltype, modelsrc=None, **kwargs):
        functor = cls.morphFuncs [ (modelsrc, celltype) ]
        return functor(**kwargs)
    
    @classmethod
    def list_morphologys(cls):
        for morphKey, morphFunctor in cls.morphFuncs.iteritems():
            print morphKey 
          
    @classmethod  
    def iteritems(cls):
        return cls.morphFuncs.iteritems()
