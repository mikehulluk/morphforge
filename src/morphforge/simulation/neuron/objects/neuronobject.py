#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
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
""" Base Class for Neuron Object """

class NeuronObject(object):

    objCnt = 0
    objNames = {}
    
    @classmethod
    def get_next_anon_name(cls):
        name = "AnonObj%04d"%NeuronObject.objCnt
        NeuronObject.objCnt += 1
        return name
    
    
    def __init__(self, simulation, name=None,  **kwargs):
        

        
        assert simulation 
        
        if not simulation in NeuronObject.objNames:
            NeuronObject.objNames[simulation] = set()
        
        if not name:
            name = NeuronObject.get_next_anon_name()
        
        assert not name in NeuronObject.objNames[simulation]
        NeuronObject.objNames[simulation].add( name )
         
         
         
        self.objName = name
        self.name = name
        
        
    def get_name(self):
        return self.objName


    def build_hoc(self, hocfile_obj):
        raise NotImplementedError()

    def build_mod(self, modfile_set):
        raise NotImplementedError()

    def get_recordable(self, *args, **kwargs):
        raise NotImplementedError()
