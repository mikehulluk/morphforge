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


from quantities_plot_new import QuantitiesAxisNew
from quantities_plot_new import QuantitiesFigureNew




class QuantitiesFigure(QuantitiesFigureNew):
    def __init__(self, *args, **kwargs):
        QuantitiesFigureNew.__init__(self, subplot_class= QuantitiesAxis, *args, **kwargs)


class QuantitiesAxis(QuantitiesAxisNew):
    def __init__(self, *args, **kwargs):
        QuantitiesAxisNew.__init__(self, *args, **kwargs)


    def plotTracePointBased(self, trace, *args, **kwargs):
        return self.plot(trace._time, trace._data, *args, **kwargs)
    def plotTracePiecewise(self, trace, *args, **kwargs):
        return self.plot(trace._time, trace._data, *args, **kwargs)

    def plotTrace(self, trace, *args, **kwargs):
        label = trace.comment
        if 'label' in kwargs:
            label = kwargs['label']
            del kwargs['label']

        plotpoints = trace.plotpoints()
        #return self.plot(plotpoints[0], plotpoints[1],'o-', *args, label=label, **kwargs)
        return self.plot(plotpoints[0], plotpoints[1], *args, label=label, **kwargs)





