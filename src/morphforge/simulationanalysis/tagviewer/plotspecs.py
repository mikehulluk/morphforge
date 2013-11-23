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
from morphforge.core import is_iterable
from morphforge import units

from morphforge.traces import TagSelector


#def is_number_roundable_to(num, n):
#    return abs(num - round(num, n)) < 0.000000001
#
#
#def get_max_rounding(num):
#    for i in range(0, 10):
#        if is_number_roundable_to(num, i):
#            return i
#    assert False
#
#def get_max_rounding_list(nums):
#    for obj in nums:
#        assert isinstance(obj, (int, float))
#    roundings = [get_max_rounding(obj) for obj in nums]
#    max_round = max(roundings)
#    return max_round
#
#
#def float_list_to_string(seq):
#    for obj in seq:
#        assert isinstance(obj, (int, float))
#    roundings = [get_max_rounding(obj) for obj in seq]
#    max_round = max(roundings)
#    return ['%.*f' % (max_round, obj) for obj in seq]


def default_legend_labeller(tr):
    if tr.comment:
        return tr.comment
    elif tr.name:
        return tr.name
    else:
        return None


class YAxisConfig(object):


    # NOTE: ynticks is deprecated! It shoudl be moved into yticks.

    def __init__(
        self,
        yunit=None,
        yrange=None,
        ylabel=None,
        yticks=None,
        yticklabels=None,
        ymargin=None,

        show_yticklabels=True,
        show_yticklabels_with_units=False,
        show_ylabel_with_units=False,
        yticklabel_quantisation=None,
        ):
        self.yrange = yrange
        self.yunit = yunit
        self.ylabel = ylabel
        self.yticklabel_quantisation=yticklabel_quantisation
        self.show_yticklabels=show_yticklabels
        self.show_yticklabels_with_units=show_yticklabels_with_units
        self.show_ylabel_with_units=show_ylabel_with_units


        # NOTE: ynticks is deprecated! It shoudl be moved into yticks.
        self.yticks = (yticks if yticks is not None else 4)

        self.yticklabels = yticklabels
        self.ymargin = ymargin


    def format_axes(self, ax):


        ax.set_ylabel(self.ylabel)
        if self.yrange is not None:
            ax.set_ylim(self.yrange)
        if self.yunit is not None:
            ax.set_display_unit(y=self.yunit)


        if self.yticks is not None:
            if isinstance( self.yticks, int):
                if self.yticks==0:
                    ax.set_yaxis_nulllocator()
                else:
                    ax.set_yaxis_maxnlocator(self.yticks)
            elif is_iterable(self.yticks):
                ax.set_yaxis_fixedlocator(self.yticks)
            else:
                assert False

        if self.yticklabels is not None:
            ax.set_yticklabels(self.yticklabels)
        else:
            ax.set_yticklabel_mode(show_ticklabels=self.show_yticklabels, include_units=self.show_yticklabels_with_units, ticklabel_quantisation=self.yticklabel_quantisation)

        #TODO: Something funky is going on and this is not making a difference
        if self.ymargin is not None:
            ax.set_ymargin(self.ymargin)


class TagPlot(object):

    def __init__(
        self,
        s,
        title=None,
        legend_labeller=default_legend_labeller,
        colors=None,
        event_marker_size=None,
        time_range=None,
        ylabel=None,
        yrange=None,
        yunit=None,
        yaxisconfig=None,
        yticks=None,
        ymargin=None,
        height_ratio=1.0,

        show_yticklabels=True,
        show_yticklabels_with_units=True, ##
        yticklabel_quantisation=None,

        overlay_traces = None
        ):

        if yaxisconfig is None:
            self.yaxisconfig = YAxisConfig(ylabel=ylabel if ylabel is not None else s,
                                         yunit=yunit,
                                         yrange=yrange,
                                         yticks=yticks,
                                         ymargin=ymargin,
                                         show_yticklabels=show_yticklabels,
                                         show_yticklabels_with_units=show_yticklabels_with_units,
                                         show_ylabel_with_units = not show_yticklabels_with_units,
                                         yticklabel_quantisation=yticklabel_quantisation
                                         )
        else:
            self.yaxisconfig = yaxisconfig

        self.title = title
        self.legend_labeller = legend_labeller
        self.colors = colors

        self.event_marker_size = event_marker_size
        self.time_range = time_range
        self.height_ratio = height_ratio

        if isinstance(s, TagSelector):
            self.selector = s
        elif isinstance(s, basestring):
            self.selector = TagSelector.from_string(s)
        else:
            assert False

        if overlay_traces is None:
            self.overlay_traces = []
        else:
            self.overlay_traces = overlay_traces


    # Used by TagViewer
    def addtrace_predicate(self, trace):
        return self.selector(trace)

    def addeventset_predicate(self, trace):
        return self.selector(trace)

    # Plot in order by name; this is normally fine, since annonymous objects
    # will be plotted in the order they were created.
    @classmethod
    def _sort_traces(cls, traces):
        return sorted(traces, key=lambda trace: trace.name)

    @classmethod
    def _sort_eventsets(cls, event_sets):
        return sorted(event_sets, key=lambda trace: trace.name)

    def _plot_trace(self, trace,  ax, index, color=None, decimate_points=False):
        plot_kwargs = {'marker':'x'}
        plot_kwargs = {}

        if self.legend_labeller  not in (None,False):
            plot_kwargs['label'] = self.legend_labeller(trace)

        if color is not None:
            plot_kwargs['color'] = color
        else:
            if self.colors:
                plot_kwargs['color'] = self.colors[index % len(self.colors)]

        if decimate_points is not None and decimate_points is not False:
            trace = trace.convert_to_fixed(decimate_points)

        plt_tr = ax.plotTrace(trace, **plot_kwargs)
        return plt_tr

    def _plot_eventset(self, eventset, ax, index):
        if len(eventset) == 0:
            return []

        plot_kwargs = {}
        if self.event_marker_size:
            plot_kwargs['markersize'] = self.event_marker_size

        if self.legend_labeller not in (None,False):
            plot_kwargs['label'] = self.legend_labeller(eventset)

        if 'label' in plot_kwargs:
            assert isinstance(plot_kwargs['label'], basestring)

        i_range = 0.2
        i_scale = i_range / len(list(eventset.times))

        data = np.array([(time.rescale("ms").magnitude, index + i * i_scale) for (i, time) in enumerate(eventset.times)])



        plot_points = ax.plot(data[:, 0] * units.ms, data[:, 1] * units.dimensionless, 'o', ms=2, **plot_kwargs)
        return plot_points




    def plot(self, ax, all_traces,  all_eventsets,  show_xlabel, show_xticklabels, show_xticklabels_with_units, show_xaxis_position, xticklabel_quantisation, is_top_plot, is_bottom_plot, xticks, time_range=None, linkage=None, decimate_points=False, xlabel=None ) :

        if self.time_range is not None:
            time_range = self.time_range

        # Which traces are we plotting (rely on a mixon class):
        trcs = [trace for trace in all_traces if self.addtrace_predicate(trace)]
        eventsets = [trace for trace in all_eventsets
                     if self.addeventset_predicate(trace)]

        # Sort and plot:
        for index, trace in enumerate(self._sort_traces(trcs)):
            #color = linkage.color_allocations.get(trace, None) if linkage else None
            color = linkage.get_trace_color(trace) if linkage else None
            self._plot_trace(trace, ax=ax, index=index, color=color, decimate_points=decimate_points)


        for index, event_set in enumerate(self._sort_eventsets(eventsets)):
            self._plot_eventset(event_set,  ax=ax, index=index+len(trcs))


        # Plot overlays:
        for tr in self.overlay_traces:
            plt_tr = ax.plotTrace(tr, linewidth=4, alpha=0.4)



        if len(trcs) == 0:
            padding = 0.5
            ax.set_yunit(1 * units.dimensionless)
            ax.set_ylim(((-padding) * units.dimensionless, (len(eventsets) - 1 + padding) * units.dimensionless))

        # Legend:
        if self.legend_labeller not in(None, False):
            import math
            import __builtin__ as BI
            ncols = BI.max(int(math.floor(len(trcs) / 5.0)), 1)
            ax.legend(ncol=ncols)

        if self.title is not None:
            ax.set_title(self.title)

        # Setup the x-axis:
        if time_range is not None:
            ax.set_xlim(time_range)

        # Setup the x-ticks
        if xticks is not None:
            if isinstance(xticks, int):
                ax.set_xaxis_maxnlocator(xticks)
            else:
                ax.set_xaxis_fixedlocator(xticks)

        # Should we plot xaxis-info at all?:
        if is_top_plot and show_xaxis_position == 'top':
            xaxis_position = 'top'
        elif is_bottom_plot and show_xaxis_position == 'bottom':
            xaxis_position = 'bottom'
        else:
            xaxis_position = None

        # Set the ticks & labels to be bottom or top
        if xaxis_position is not None:
            ax.set_xaxis_ticks_position(xaxis_position)
            ax.set_xaxis_label_position(xaxis_position)

        # Plot the axis-label, if
        # show_ticklabels=='all' OR show_ticklabels=='only-once' AND xaxis_position is not None:
        if show_xlabel == 'all' or show_xlabel == 'only-once' and xaxis_position is not None and xlabel:
            ax.set_xlabel(xlabel)
        else:
            ax.set_xlabel('')

        # Similarly, plot the axis-ticklabel, if
        show_xticks = show_xticklabels == 'all' or (show_xticklabels == 'only-once' and xaxis_position is not None)
        ax.set_xticklabel_mode(show_ticklabels=show_xticks, include_units=show_xticklabels_with_units, ticklabel_quantisation=xticklabel_quantisation)

        # Setup the y-axis:
        self.yaxisconfig.format_axes(ax)

        # Turn the grid on:
        ax.grid('on')


