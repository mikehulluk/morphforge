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
from morphforge.simulation.core.networks import PreSynapticMechanism,\
    PreSynapticTypes
from morphforge.traces.eventset import EventSet



 
    
class PreSynapticMech_VoltageThreshold(PreSynapticMechanism):
    
    def __init__(self, celllocation, voltageThreshold, delay, weight ):
        self.celllocation = celllocation  
        self.voltageThreshold = voltageThreshold  
        self.delay = delay  
        self.weight = weight
    
    
    def getPreSynapticCellLocation(self):
        return self.celllocation    

    def getPreSynapticCell(self):
        return self.celllocation.cell

    def get_type(self):
        return PreSynapticTypes.Cell


class PreSynapticMech_TimeList(PreSynapticMechanism):

    def __init__(self, timeList,  weight ):
        PreSynapticMechanism.__init__(self)
        
        #Convert into an event set
        if not isinstance(timeList,EventSet):
            timeList = EventSet(timeList)
            
        
        self.timeList = timeList  
        self.weight = weight
       
    def getPreSynapticCell(self):
        return None   
        
    def get_type(self):
        return PreSynapticTypes.FixedTiming