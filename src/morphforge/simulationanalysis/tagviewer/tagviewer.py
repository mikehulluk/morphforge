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
#from morphforge.core import unit
from morphforge.simulation.base import SimulationResult
from morphforge.core.quantities import mV, ms, Quantity
from mhlibs.quantities_plot import QuantitiesFigure
from plotspecs import TagPlot
from morphforge.traces import TraceFixedDT
from morphforge.traces import TraceVariableDT
from morphforge.traces import TracePiecewise
from morphforge.traces.eventset import EventSet
from morphforge.core import quantities as pq

# pylint: disable=W0108
# (Suppress warning about 'unnessesary lambda functions')

#def _resolve_time_range(time_range):
#    # Sort out the time_range:
#    if time_range is not None:
#        if isinstance(time_range, (tuple, list, Quantity)):
#            if len(time_range) == 2:
#                if isinstance(time_range[0], Quantity):
#                    pass
#                else:
#                    assert False
#                    time_range = time_range * ms
#        else:
#            assert False
#    return time_range




class DefaultTagPlots(object):
    Voltage =            TagPlot(s="Voltage", ylabel='Voltage', yrange=(-80*mV, 50*mV), yunit=pq.millivolt )
    CurrentDensity =     TagPlot(s="CurrentDensity", ylabel='CurrentDensity', yunit=pq.milliamp / pq.cm2 )
    Current =            TagPlot(s="Current", ylabel='Current', yunit=pq.picoamp)
    Conductance =        TagPlot(s="Conductance", ylabel="Conductance")
    ConductanceDensity = TagPlot(s="ConductanceDensity", ylabel="ConductanceDensity", yunit=pq.milli * pq.siemens / pq.cm2 )
    StateVariable =      TagPlot(s="StateVariable", ylabel="StateVariable")
    StateVariableTau =   TagPlot(s="StateTimeConstant", yunit=pq.millisecond, ylabel="Time Constant")
    StateVariableInf =   TagPlot(s="StateSteadyState", ylabel="Steady State")
    Event =              TagPlot(s="Event", ylabel="Events")





class TagViewer(object):

    MPL_AUTO_SHOW = True

    _default_plot_specs = (
        DefaultTagPlots.Voltage,
        DefaultTagPlots.CurrentDensity,
        DefaultTagPlots.Current,
        DefaultTagPlots.Conductance,
        DefaultTagPlots.ConductanceDensity,
        DefaultTagPlots.StateVariable,
        DefaultTagPlots.StateVariableTau,
        DefaultTagPlots.StateVariableInf,
        DefaultTagPlots.Event,
       )

    _default_fig_kwargs = {'figsize': (12, 8) }

    def __init__(
        self,
        srcs,
        fig_kwargs=None,
        plots=None,
        figtitle=None,
        show=True,
        save=None,
        linkage=None,
        timerange=None,
        additional_plots=None,
        share_x_labels=True,
        mpl_tight_bounds=False,
        ):

        if fig_kwargs is None:
            fig_kwargs = self._default_fig_kwargs

        self.linkage = linkage


        if not is_iterable(srcs):
            srcs = [srcs]

        # For each type of input (in 'srcs'); this should return a list of traces:
        self.all_trace_objs = []
        self.all_event_set_objs = []
        trace_extractors = {
            SimulationResult:   lambda obj: self.all_trace_objs.extend(obj.traces),
            TraceFixedDT:       lambda obj: self.all_trace_objs.append(obj),
            TraceVariableDT:    lambda obj: self.all_trace_objs.append(obj),
            TracePiecewise:     lambda obj: self.all_trace_objs.append(obj),
            EventSet:           lambda obj: self.all_event_set_objs.append(obj)
                            }

        for obj in srcs:
            tr_extractor = trace_extractors[type(obj)]
            tr_extractor(obj)

        # Use the new PlotSpec architecture:
        # Filter out which plots are actually going to display something,
        # and filter out the rest:
        plots = plots if plots is not None else TagViewer._default_plot_specs

        if additional_plots:
            plots = tuple(list(plots) + list(additional_plots))

        self.plot_specs = [plotspec for plotspec in plots if
                            [tr for tr in self.all_trace_objs if plotspec.addtrace_predicate(tr)] or  \
                            [evset for evset in self.all_event_set_objs if plotspec.addeventset_predicate(evset)] \
                          ]


        self.fig_kwargs = fig_kwargs
        self.figtitle = figtitle
        self.mpl_tight_bounds = mpl_tight_bounds

        self.timerange = timerange
        self.share_x_labels = share_x_labels

        self.fig = None
        self.subaxes = []
        self.create_figure()

        # 'svae' is deprecated'
        assert save is None, ' "save" parameter is deprecated (15 July 2012)'
        # Save the figure:
        # if save:
        #    PM.save_figure(figtitle)

        if TagViewer.MPL_AUTO_SHOW and show:
            import pylab
            pylab.show()

    def create_figure(self):
        self.fig = QuantitiesFigure(**self.fig_kwargs)

        # Add a title to the plot:
        if self.figtitle:
            self.fig.suptitle(self.figtitle)

        # Work out what traces are on what graphs:
        plotspec_to_traces = dict([(plot_spec, [tr for tr in self.all_trace_objs if plot_spec.addtrace_predicate(tr)]) for plot_spec in self.plot_specs ])
        if self.linkage:
            self.linkage.process(plotspec_to_traces)

        n_plots = len(self.plot_specs)

        for (i, plot_spec) in enumerate(self.plot_specs):

            # Create the axis:
            ax = self.fig.add_subplot(n_plots, 1, i + 1)
            ax.set_xunit(pq.millisecond)
            ax.set_xmargin(0.05)
            ax.set_ymargin(0.05)

            # Leave the plotting to the PlotSpecification
            is_bottom_plot = i == n_plots - 1
            plot_xaxis_details = is_bottom_plot or not self.share_x_labels
            plot_spec.plot(ax=ax, all_traces=self.all_trace_objs, all_eventsets=self.all_event_set_objs, time_range=self.timerange, linkage=self.linkage, plot_xaxis_details=plot_xaxis_details)

            # Save the Axis:
            self.subaxes.append(ax)

        if self.mpl_tight_bounds:
            import pylab
            try:
                pylab.tight_layout()
            except AttributeError:
                pass  # This is version specfic
            except ValueError:
                pass # Top can't be less than bottom


