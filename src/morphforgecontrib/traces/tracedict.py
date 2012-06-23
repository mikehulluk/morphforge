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


def fig_plot_local(x=None, y=None, title=None, xlims=None, ylims=None, xlabel=None, ylabel=None, figsize=None, legend=False, **kwargs):
    from pylab import figure

    f = figure() if not figsize else figure(figsize=figsize)
    if title: f.suptitle(title)
    ax = f.add_subplot(111)
    if x != None and y != None:
        ax.plot(x, y, **kwargs)
        if xlims: ax.set_xlim(xlims[0], xlims[1])
        if ylims: ax.set_ylim(ylims[0], ylims[1])
    if legend: ax.legend()
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    return ax




class TraceDict(object):

    def __init__(self, data=None):
        self.data = {}
        if data:
            for k, v in data:
                self[k] = v

    def __setitem__(self, k, v):
        self.data[k] = v

    def __getitem__(self, k):
        return self.data[k]


    def _plot_trace_old(self, k, v, ax, legend_func, xunits,yunits): #, xUnits, yUnits):
        #data_line_curve = ax.plot( expCurrentTrace.time, v.data, label="Cmd: %2.2f mV"%cmdVoltage)
        if legend_func:
            data_line_curve = ax.plot(v._time.rescale(xunits), v._data.rescale(yunits) , label=legend_func(k, v))[0]
            return data_line_curve

    def Plot(self, fig=None, ax=None, title="Untitled", xlabel_prefix="Time", ylabel_prefix="", xunits="ms", yunits=None, legend_func=None,):
        assert yunits

        if fig == None and ax == None:
            ax = fig_plot_local(title=title,
                        xlabel=xlabel_prefix + "(" + str(xunits) + ")",
                        ylabel=ylabel_prefix + "(" + str(yunits) + ")",
                        figsize=(9, 4))


        #print self.baseunit
        lines = {}
        #for k,v in self.data.iteritems():
        for k in sorted(self.data.keys()):
            v = self.data[k]
            lines[k] = self._plot_trace_old(k, v, ax, legend_func=legend_func,xunits=xunits,yunits=yunits)

        if legend_func: ax.legend()
        return ax, lines


    def iteritems(self):
        return  self.data.iteritems()
