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

from morphforge.core import is_iterable
from morphforge.core import unit
from morphforge.simulation.base import SimulationResult
from morphforge.core.quantities import mV, ms, Quantity
from mhlibs.quantities_plot import QuantitiesFigure
from plotspecs import PlotSpec_DefaultNew
from morphforge.traces import  Trace_FixedDT, Trace_VariableDT, Trace_Piecewise
from morphforge.traces.eventset import EventSet
from morphforge.core import quantities as pq
from mreorg.scriptplots import PM





def _resolve_time_range(time_range):
    # Sort out the time_range:
    if time_range is not None:
        if  isinstance(time_range, (tuple, list, Quantity) ):
            if len(time_range) == 2:
                if isinstance(time_range[0], Quantity ):
                    pass
                else:
                    assert False
                    time_range = time_range * ms
        else:
            assert False
    return time_range




class DefaultPlotSpec:
    Voltage =            PlotSpec_DefaultNew( s="Voltage", ylabel='Voltage', yrange=(-80*mV,50*mV), yunit=pq.millivolt  )
    CurrentDensity =     PlotSpec_DefaultNew( s="CurrentDensity", ylabel='CurrentDensity', yunit=pq.milliamp/pq.cm2  )
    Current =            PlotSpec_DefaultNew( s="Current", ylabel='Current',yunit=pq.picoamp )
    Conductance =        PlotSpec_DefaultNew( s="Conductance", ylabel="Conductance" )
    ConductanceDensity = PlotSpec_DefaultNew( s="ConductanceDensity", ylabel="ConductanceDensity", yunit=pq.milli * pq.siemens / pq.cm2  )
    StateVariable =      PlotSpec_DefaultNew( s="StateVariable", ylabel="StateVariable" )
    StateVariableTau =   PlotSpec_DefaultNew( s="StateTimeConstant",yunit=pq.millisecond, ylabel="Time Constant"  )
    StateVariableInf =   PlotSpec_DefaultNew( s="StateSteadyState", ylabel="Steady State" )
    Event =              PlotSpec_DefaultNew( s="Event", ylabel="Events" )





class TagViewer(object):

    MPL_AUTO_SHOW = True


    defaultPlotSpecs = (
        DefaultPlotSpec.Voltage,
        DefaultPlotSpec.CurrentDensity,
        DefaultPlotSpec.Current,
        DefaultPlotSpec.Conductance,
        DefaultPlotSpec.ConductanceDensity,
        DefaultPlotSpec.StateVariable,
        DefaultPlotSpec.StateVariableTau,
        DefaultPlotSpec.StateVariableInf,
        DefaultPlotSpec.Event,
        )



    def __init__(self,
                 input,
                 fig_kwargs = {'figsize': (12, 8)},
                 timeranges=(None,),
                 plotspecs = None,
                 #post_ax_functors= None,
                 figtitle = None,
                 show=True,
                 save=True,
                 linkage = None,
                 timerange=None,
                 additional_plotspecs = None,
                 share_x_labels=True,
                 mpl_tight_bounds = True
                 ):

        self.linkage = linkage


        if timerange is not None:
            timeranges = [timerange,]


        if not is_iterable( input ):
            input = [input]



        # For each type of input; this should return a list of traces:
        self.allTraceObjs = []
        self.allEventSetObjs = []
        trace_extractors = {
            SimulationResult:       lambda i: self.allTraceObjs.extend( i.traces ),
            Trace_FixedDT:          lambda i: self.allTraceObjs.append( i ),
            Trace_VariableDT:       lambda i: self.allTraceObjs.append( i ),
            Trace_Piecewise:        lambda i: self.allTraceObjs.append( i ),
            EventSet:               lambda i: self.allEventSetObjs.append(i)
                            }

        for i in input:
            tr_extractor = trace_extractors[ type(i) ]
            tr_extractor(i)


        # Use the new PlotSpec architecture:
        # Filter out which plotspecs are actually going to display something,
        # and filter out the rest:
        plotspecs = plotspecs if plotspecs is not None else TagViewer.defaultPlotSpecs

        if additional_plotspecs:
            plotspecs = tuple( list(plotspecs) + list(additional_plotspecs) )

        self.plot_specs = [ sp for sp in plotspecs if
                            [ tr for tr in self.allTraceObjs if sp.addtrace_predicate(tr)] or  \
                            [ evset for evset in self.allEventSetObjs if sp.addeventset_predicate(evset)] \
                           ]


        self.fig_kwargs = fig_kwargs
        self.figtitle = figtitle
        self.mpl_tight_bounds = mpl_tight_bounds

        #self.post_ax_functors = post_ax_functors

        self.timeranges = timeranges
        self.share_x_labels = share_x_labels


        self.fig = None
        self.subaxes = []
        self.create_figure()



        # Save the figure:
        if save:
            PM.save_figure( figtitle )


        if TagViewer.MPL_AUTO_SHOW and show:
            import pylab
            pylab.show()



    def create_figure(self):
        self.fig = QuantitiesFigure(**self.fig_kwargs)


        # Add a title to the plot:
        if self.figtitle:
            self.fig.suptitle(self.figtitle)


        # Work out what traces are on what graphs:
        ps_to_traces = dict([ (ps,[tr for tr in self.allTraceObjs if ps.addtrace_predicate(tr) ]) for ps in self.plot_specs  ])
        if self.linkage:
            self.linkage.process(ps_to_traces)


        n_time_ranges = len(self.timeranges)
        n_plots = len(self.plot_specs)


        #time_axis = None

        for i, plot_spec in enumerate( self.plot_specs ):

            print 'Plotting For PlotSpec:', plot_spec

            for iT, time_range in enumerate(self.timeranges):


                time_range = _resolve_time_range(time_range)

                # Create the axis:
                ax = self.fig.add_subplot(n_plots, n_time_ranges, i*n_time_ranges + iT  + 1 )
                ax.set_xunit(pq.millisecond)

                # Leave the plotting to the PlotSpecification
                is_bottom_plot = i==n_plots-1
                plot_xaxis_details = is_bottom_plot or not self.share_x_labels
                plot_spec.plot( ax=ax, all_traces=self.allTraceObjs, all_eventsets=self.allEventSetObjs, time_range=time_range, linkage=self.linkage, plot_xaxis_details=plot_xaxis_details )

                # Save the Axis:
                self.subaxes.append(ax)


        if self.mpl_tight_bounds:
            import pylab
            pylab.tight_layout()



