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
from morphforge.core.quantities import convertToUnit
from morphforge.constants import StdRec
    

from stimulation import  Stimulation     

class VoltageClamp(Stimulation):
    class Recordables():
        Current = StdRec.Current
        


class VoltageClampStepChange(VoltageClamp):
    
    def __init__(self, name, dur1, amp1, celllocation, dur2=0, dur3=0, amp2=0, amp3=0, rs=0.1):
        super(VoltageClamp, self).__init__(name=name, celllocation=celllocation)
        
        self.dur1 = convertToUnit(dur1, defaultUnit="ms")
        self.dur2 = convertToUnit(dur2, defaultUnit="ms")
        self.dur3 = convertToUnit(dur3, defaultUnit="ms")
        
        self.amp1 = convertToUnit(amp1, defaultUnit="mV")
        self.amp2 = convertToUnit(amp2, defaultUnit="mV")
        self.amp3 = convertToUnit(amp3, defaultUnit="mV")
        self.rs = convertToUnit( rs, defaultUnit="MOhm")
