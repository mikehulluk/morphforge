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

import numpy as np
from morphforge.core.quantities.fromcore import unit
import quantities as pq

from morphforge.traces import TagSelector


def default_legend_labeller(tr):
    if tr.comment:
        return tr.comment
    elif tr.name:
        return tr.name
    else:
        return None






class YAxisConfig(object):
    def __init__(self, yunit=None, yrange=None, ylabel=None, yticks=None, yticklabels=None, ymargin=None, ynticks=None):
        self.yrange = yrange
        self.yunit = yunit
        self.ylabel = ylabel
        self.ynticks= ynticks if ynticks is not None else 5
        pass

    def format_axes(self, ax):
        ax.set_ylabel( self.ylabel )
        if self.yrange is not None:
            ax.set_ylim( self.yrange )
        if self.yunit is not None:
            ax.set_display_unit(y=self.yunit)

        #ax.xaxis.set_major_locator( mpl.ticker.MaxNLocator(4) )
        ax.set_yaxis_maxnlocator(self.ynticks)


class PlotSpec_DefaultNew( object):

    def __init__(self, s, title=None, legend_labeller=default_legend_labeller, colors=None, event_marker_size=None, time_range=None, ylabel=None, yrange=None, yunit=None, ynticks=None, yaxisconfig=None):
        #self.yrange = yrange
        #self.yunit = yunit
        #self.ylabel = ylabel if ylabel else s

        if yaxisconfig is None:
            self.yaxisconfig=YAxisConfig(ylabel=ylabel if ylabel else s,
                                         yunit=yunit,
                                         yrange=yrange,
                                         ynticks=ynticks)
        else:
            self.yaxisconfig = yaxisconfig



        self.title = title
        self.legend_labeller = legend_labeller
        self.colors = colors

        self.event_marker_size = event_marker_size
        self.time_range = time_range


        if isinstance(s, TagSelector):
            self.selector = s
        elif isinstance(s, basestring):
            self.selector = TagSelector.from_string(s)
        else:
            assert False


    #def _get_selector_ylabel(self):
    #    return self.ylabel

    # Used by TagViewer
    def addtrace_predicate(self, trace):
        return self.selector(trace)
    def addeventset_predicate(self, trace):
        return self.selector(trace)


    # Plot in order by name; this is normally fine, since annonymous objects
    # will be plotted in the order they were created.
    def _sort_traces(self, traces):
        return sorted( traces, key=lambda t : t.name)
    def _sort_eventsets(self, event_sets):
        return sorted( event_sets, key=lambda t : t.name)


    def _plot_trace(self, trace,  ax, index, color=None):
        plot_kwargs = {}


        if self.legend_labeller is not None:
            plot_kwargs['label'] = self.legend_labeller(trace)


        if color is not None:
            plot_kwargs['color'] = color
        else:
            if self.colors:
                plot_kwargs['color'] = self.colors[ index % len(self.colors) ]

        plt_tr =  ax.plotTrace(trace, **plot_kwargs)
        return plt_tr

    def _plot_eventset(self, eventset, ax, index):
        if len(eventset) == 0:
            return []


        plot_kwargs = {}
        if self.event_marker_size:
            plot_kwargs['markersize'] = self.event_marker_size

        if self.legend_labeller is not None:
            plot_kwargs['label'] = self.legend_labeller(eventset)


        if 'label' in plot_kwargs:
            assert isinstance(plot_kwargs['label'], basestring)

        i_range = 0.2
        i_scale = i_range / len( list(eventset.times) )

        data = np.array( [ (t.rescale("ms").magnitude,index+i*i_scale) for i,t in enumerate(eventset.times) ] )



        from morphforge.stdimports import pq
        p= ax.plot( data[:,0] * pq.ms, data[:,1] * pq.dimensionless ,'o',ms=2, **plot_kwargs )
        return p




    def plot(self, ax, all_traces,  all_eventsets, plot_xaxis_details, time_range=None, linkage=None, ) :
        if self.time_range is not None:
            time_range = self.time_range

        # Which traces are we plotting (rely on a mixon class):
        trcs = [tr for tr in all_traces if self.addtrace_predicate(tr)]
        eventsets = [tr for tr in  all_eventsets if self.addeventset_predicate(tr)]


        # Sort and plot:
        for index, trace in enumerate( self._sort_traces(trcs) ):
            color = linkage.color_allocations.get(trace, None) if linkage else None
            self._plot_trace( trace, ax=ax, index=index, color=color)


        for index, event_set in enumerate( self._sort_eventsets(eventsets) ):
            self._plot_eventset( event_set,  ax=ax, index=index+len(trcs) )

            #ax.set_ylim( ( (-0.5) * pq.dimensionless, (len(eventsets)+0.5) * pq.dimensionless ) )


        if len(trcs) == 0:
            padding =0.5
            ax.set_yunit( 1*pq.dimensionless )
            ax.set_ylim( ( (-padding) * pq.dimensionless, (len(eventsets)-1+padding) * pq.dimensionless ) )

        #Legend:
        if self.legend_labeller is not None:
            import math
            import __builtin__ as BI
            ncols = BI.max( int( math.floor( len(trcs) / 5.0) ), 1)
            ax.legend(ncol=ncols)

        if self.title:
            ax.set_title( self.title )

        # Label up the axis:
        if plot_xaxis_details:
            ax.set_xlabel('Time')
        else:
            ax.set_xlabel('')
            ax.set_xticklabels([])

        #ax.set_xunit( unit('ms') )
        #print ax.xyUnitBase[0]
        #print ax.xyUnitDisplay[0]
        #assert False


        # Setup the y-axis:
        #ax.set_ylabel( self.yaxisconfig.ylabel )
        self.yaxisconfig.format_axes(ax)



        if time_range is not None:
            #print 'Setting Time Range', time_range
            ax.set_xlim( time_range )
        #if self.yaxisconfig.yrange is not None:
        #    ax.set_ylim( self.yaxisconfig.yrange )

        #if self.yunit is not None:
        #    #print 'Setting Yunit', self.yaxisconfig.yunit
        #    ax.set_display_unit(y=self.yaxisconfig.yunit)

        # Turn the grid on:
        ax.grid('on')
