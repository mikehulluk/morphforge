 
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

from morphforge.simulation.base.networks import SynapticTrigger
from morphforge.simulation.base.networks import PreSynapticTypes
from morphforge.traces.eventset import EventSet


class SynapticTriggerByVoltageThreshold(SynapticTrigger):

    def __init__(self, cell_location, voltage_threshold, delay, **kwargs):
        super(SynapticTriggerByVoltageThreshold, self).__init__(**kwargs)
        self.cell_location = cell_location
        self.voltage_threshold = voltage_threshold
        self.delay = delay

    def get_presynaptic_cell_location(self):
        return self.cell_location

    def get_presynaptic_cell(self):
        return self.cell_location.cell

    def get_type(self):
        return PreSynapticTypes.Cell

    def get_summary_string(self):
        return '%s: [threshold: %s]'%( self.cell_location.get_location_description_str(), self.voltage_threshold )



class SynapticTriggerAtTimes(SynapticTrigger):

    def __init__(self, time_list, **kwargs):
        super(SynapticTriggerAtTimes, self).__init__(**kwargs)

        # Convert into an event set
        if not isinstance(time_list, EventSet):
            time_list = EventSet(time_list)

        self.time_list = time_list

    def get_presynaptic_cell(self):
        return None

    def get_type(self):
        return PreSynapticTypes.FixedTiming


    def get_summary_string(self):
        return 'At times: %s (ms)'%( self.time_list.times_in_np_array_ms() )
