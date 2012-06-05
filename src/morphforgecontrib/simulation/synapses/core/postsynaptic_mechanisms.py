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
from morphforge.simulation.core.networks import PostSynapticMech




class PostSynapticMech_ExpSyn(PostSynapticMech):
    def __init__(self, celllocation, tau, eRev):
        super(PostSynapticMech_ExpSyn, self).__init__(celllocation)
        self.tau = tau
        self.eRev = eRev

class PostSynapticMech_Exp2Syn(PostSynapticMech):
    def __init__(self, celllocation, tauOpen, tauClosed, eRev, popening=1.0):
        super(PostSynapticMech_Exp2Syn, self).__init__(celllocation)
        self.tauOpen = tauOpen
        self.tauClosed = tauClosed
        self.eRev = eRev
        self.popening = popening

class PostSynapticMech_Exp2SynNMDA(PostSynapticMech):
    def __init__(self, celllocation, tauOpen, tauClosed, eRev, popening=1.0, vdep=True):
        super(PostSynapticMech_Exp2SynNMDA, self).__init__(celllocation)
        self.tauOpen = tauOpen
        self.tauClosed = tauClosed
        self.eRev = eRev
        self.popening = popening
        self.vdep=vdep
        #extracellular_mg = extracellular_mg
        
