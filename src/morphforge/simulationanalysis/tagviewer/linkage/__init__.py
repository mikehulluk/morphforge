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

import re
from collections import defaultdict
from itertools import chain
import __builtin__ as bi



def _get_collision_of_color_index_for_group(colorIndex, group, plotspec_to_traces_dict, allocated_trace_colors):

    collisions = 0
    for (_ps, ps_traces) in plotspec_to_traces_dict.iteritems():

        ps_allocated_indices = [allocated_trace_colors.get(tr, None) for tr in ps_traces ]
        ps_allocated_indices = [a for a in ps_allocated_indices if a is not None]
        clashes = ps_allocated_indices.count(colorIndex)

        # Does this group have anything that would go into this plot-spec?
        # If not, then it doesn't matter about collisions!
        n_group_in_ps = set(group) & set(ps_traces)

        if len(n_group_in_ps) > 0:
            collisions += clashes

    return collisions + 1




class LinkageRule(object):
    def __call__(self, all_traces):
        """returns a sequence of tuples, containing the traces that are connected to each other"""
        raise NotImplementedError()


class LinkageRuleTagRegex(object):

    def __init__(self, regex):
        self.regex = re.compile(regex, re.VERBOSE)

    def get_match_tags(self, tr):
        matches = []
        for tag in tr.tags:
            if self.regex.match(tag):
                matches.append(tag)
        return matches

    def __call__(self, all_traces):
        grps = defaultdict(list)

        for trace in all_traces:
            match_tags = self.get_match_tags(trace)
            for matchtag in match_tags:
                grps[matchtag].append(trace)
        return grps.values()

from morphforge.traces.tags import TagSelector

class LinkageRuleTag(object):
    def __init__(self, tagselector):
        if isinstance(tagselector, basestring):
            self._tagselector = TagSelector.from_string(tagselector)

        else:
            self._tagselector = tagselector


    def __call__(self, all_traces):
        matches = [trace for trace in all_traces if self._tagselector(trace)]
        if len(matches) in [0, len(all_traces)]:
            assert False, 'All or none selected, an error has probably been made!'
        #print 'matches', matches
        #assert False
        return [matches]



class AbstrLinkage(object):
    """ Linkage classes are used to choose colours for TagViewer plots.

    They are called 'linkages' beacuse they make links between traces across
    different plots. For example, supposing we have graphs of membrane voltage,
    and current flows, then we may wish to specify that all the traces of
    Neuron1 are in blue and all those of Neuron2 are in green.
    """

    def process(self, plotspec_to_traces_dict):
        """ Preprocessing of linkages before plotting.
        TagViewer will assign traces to the plotspecs, then call this function
        """
        raise NotImplementedError()

    def get_trace_color(self, trace):
        """Returns the colour code for the *trace"""
        raise NotImplementedError()



#class ColorAssigner(object):
#    def __init__(self, color_rules):
#        self._color_rules = color_rules





class StandardLinkages(object):
    def __init__(self, linkages_explicit=None, linkage_rules=None, color_rules=None):
        self._linkages_explicit = linkages_explicit or []

        self._color_cycle = ['blue', 'green', 'red', 'cyan', 'yellow', 'black']

        self.linkage_rules = (linkage_rules if linkage_rules else [])
        self._color_allocations = None

        self._color_assigner = (color_rules if color_rules else [])


    def get_trace_color(self, tr):
        return self._color_allocations[tr]

    def _get_linkages_from_rules(self, all_traces):
        links = chain(*[link_rule(all_traces) for link_rule in self.linkage_rules])
        return list(links)

    def process(self, plotspec_to_traces_dict):
        """ Assign colours to the traces. We aim to minise color clashes, but
        still only use one color for a given trace, even if it appears on multiple plots.

        1/ We build a graph, in which each node represents trace, and edges represent 'linkage'
        2/ We look at the connected components, i.e. the traces that should all have the same color_indices
        3/ If we have more groups than colours, then we allocate 'color indices to these groups based 
        on mimising color collisions the plots.
        
        ## TODO: 4/ Actual colour is assigned by the color_assigner.

        """

        import networkx

        all_traces = set(chain(*plotspec_to_traces_dict.values()))

        allocated_trace_colors = {}
        color_indices = range(len(self._color_cycle))

        G = networkx.Graph()
        # Add a node per trace:
        for trace in all_traces:
            G.add_node(trace)

        # Add the edges:
        all_links = self._linkages_explicit + self._get_linkages_from_rules(all_traces)
        for link in all_links:
            (first, remaining) = (link[0], link[1:])
            for r in remaining:
                G.add_edge(first, r)

        groups = networkx.connected_components(G)

        for grp in sorted(groups, key=lambda g: (len(g), id(g[0])), reverse=True) :

            #Calculate how many collisions we would have for each allocation:
            def index_score(i):
                s = _get_collision_of_color_index_for_group(colorIndex=i,
                                                        group=grp,
                                                        plotspec_to_traces_dict=plotspec_to_traces_dict,
                                                        allocated_trace_colors=allocated_trace_colors)
                return s

            new_index = bi.min(color_indices, key=index_score)
            # Allocate to colorIndex:
            for g in grp:
                allocated_trace_colors[g] = new_index


        # We have now assigned a color_index to each group, all that now remains

        # Make the allocation from index to colors:
        self._color_allocations = {}
        for trace in all_traces:
            self._color_allocations[trace] = self._color_cycle[allocated_trace_colors[trace]]





#l = StandardLinkages(linkages_explicit = [(trI1, trV1, trG1), (trI2, trV2, trG2)])
#
##TagViewer([trI1, trV1, trG1, trI2, trV2, trG2], linkage=None)
#TagViewer([trI1, trV1, trG1, trI2, trV2, trG2], linkage=l)
#TagViewer([trI1, trV1, trG1, trI2, trV2, trG2], linkage=StandardLinkages(linkage_rules=[LinkageRuleTagRegex("Sim(\d+)")]) )


