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




import morphforge.stdimports as mf
from mhlibs.quantities_plot import QuantitiesFigure
import pylab

from morphforge.stdimports import qty, reduce_to_variable_dt_trace


t1 = mf.TraceGenerator.generate_flat(value='1:mV')
#t2 = mf.TraceGenerator.generate_flat(value='0.0015:V')
t2 = mf.TraceGenerator.generate_ramp(value_start='0.0015:V', value_stop='2.5:mV', npoints=20)



f = QuantitiesFigure()
ax = f.add_subplot(111)
ax.plotTrace(t1, marker='x')
ax.plotTrace(t2, marker='o')
ax.plotTrace(t1+t2, marker='<')
ax.plotTrace((t2+t2)*3.0+qty('0.03:V'), marker='<')

t1 = mf.fixed_to_variable_dt_trace(t1, '0.01:mV')
ax.plotTrace(t1, marker='>')
ax.legend()

pylab.show()

