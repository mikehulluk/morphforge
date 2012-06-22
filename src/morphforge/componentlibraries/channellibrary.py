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
class ChannelLibrary(object):
    
    channels = dict()
    
    
    @classmethod
    def register_channel(cls,channeltype , chlFunctor,  modelsrc=None, celltype=None ):
        assert modelsrc or celltype
        key = modelsrc, celltype , channeltype
        assert not key in cls.channels
        cls.channels[ key ] = chlFunctor
        
        
        
    @classmethod        
    def get_channel_functor(cls, channeltype, modelsrc=None, celltype=None,):
        return cls.channels [ (modelsrc, celltype, channeltype) ]
    
    @classmethod        
    def get_channel(cls, channeltype, env, modelsrc=None, celltype=None, ):
        functor = cls.channels [ (modelsrc, celltype, channeltype) ]
        return functor(env=env)
    
    @classmethod
    def list_channels(cls):
        for chlType, chl in cls.channels.iteritems():
            print chlType 
          
    @classmethod  
    def iteritems(cls):
        return cls.channels.iteritems()
