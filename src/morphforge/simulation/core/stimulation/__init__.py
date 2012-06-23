#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer. 
#  - Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------


from morphforge.core.quantities.fromcore import unit
from morphforge.constants.stdrecordables import StdRec

class Stimulation(object):
    def __init__(self, name, celllocation):
        self.name = name
        self.celllocation = celllocation

class CurrentClamp(Stimulation):
    class Recordables(object):
        Current = StdRec.Current


class VoltageClamp(Stimulation):
    class Recordables():
        Current = StdRec.Current


class CurrentClampStepChange(CurrentClamp):

    def __init__(self, name, amp, dur, delay, celllocation, **kwargs):
        super(CurrentClamp, self).__init__(name=name, celllocation=celllocation)
        self.amp = unit(amp)
        self.dur = unit(dur)
        self.delay = unit(delay)



class VoltageClampStepChange(VoltageClamp):

    def __init__(self, name, dur1, amp1, celllocation, dur2="0:ms", dur3="0:ms", amp2="0:mV", amp3='0:mV', rs="0.1:MOhm"):
        super(VoltageClamp, self).__init__(name=name, celllocation=celllocation)

        self.dur1 = unit(dur1)
        self.dur2 = unit(dur2)
        self.dur3 = unit(dur3)

        self.amp1 = unit(amp1)
        self.amp2 = unit(amp2)
        self.amp3 = unit(amp3)
        self.rs = unit( rs)



__all__ = [
    "CurrentClamp",
    "VoltageClamp",
    "CurrentClampStepChange",
    "VoltageClampStepChange",
    "Stimulation"
]
