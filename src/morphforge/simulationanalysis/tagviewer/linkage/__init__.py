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



def _get_collision_of_color_index_for_group(colorIndex, group, ps_to_traces_dict, allocatedTraceColors):

    collisions = 0
    for (ps, ps_traces) in ps_to_traces_dict.iteritems():

        ps_allocated_indices = [ allocatedTraceColors.get(tr,None) for tr in ps_traces  ]
        ps_allocated_indices = [ a for a in ps_allocated_indices if a is not None]
        clashes = ps_allocated_indices.count( colorIndex )

        # Does this group have anything that would go into this plot-spec?
        # If not, then it doesn't matter about collisions!
        nGroupInPS = set(group) & set(ps_traces)

        if len(nGroupInPS) > 0:
            collisions += clashes

    return collisions + 1



class LinkageRuleTagRegex(object):
    def __init__(self, regex):
        self.regex = re.compile(regex, re.VERBOSE)

    def getMatchTags(self, tr):
        tMatches = []
        for t in tr.tags:
            if self.regex.match(t):
                tMatches.append(t)
        return tMatches
        
    def __call__(self,allTraces):
        grps = defaultdict(list)

        for tr in allTraces:
            matchTags = self.getMatchTags(tr)
            for mT in matchTags:
                grps[mT].append(tr)

        return grps.values()
        #matches = [ tr for tr in allTraces]
        #return []



class StandardLinkages(object):
    def __init__(self, linkages_explicit=None, linkage_rules=None):
        self.linkages_explicit = linkages_explicit or []

        self.color_cycle = ['blue','green','red','cyan','yellow','black' ]

        self.linkage_rules = linkage_rules if linkage_rules else []


    def getLinkagesFromRules(self, allTraces):
        links = chain(*[link_rule(allTraces) for link_rule in self.linkage_rules])
        return list(links)



    def process(self, ps_to_traces_dict):
        import networkx as nx

        allTraces = set(chain(*ps_to_traces_dict.values()))

        allocatedTraceColors = {}
        colorIndices = range(len(self.color_cycle))

        G = nx.Graph()
        # Add a node per trace:
        for tr in allTraces:
            G.add_node(tr)

        # Add the edges:
        all_links = self.linkages_explicit + self.getLinkagesFromRules(allTraces)
        for link in all_links:
            (first, remaining) = (link[0], link[1:])
            for r in remaining:
                G.add_edge(first, r)

        groups = nx.connected_components(G)

        for grp in sorted(groups, key=lambda g:(len(g),id(g[0]) ) , reverse=True) :
            #print 'Allocating', ''.join( g.name for g in grp)
            #Calculate how many collisions we would have for each allocation:
            def indexScore(i):
                s = _get_collision_of_color_index_for_group(colorIndex=i,
                                                        group=grp,
                                                        ps_to_traces_dict=ps_to_traces_dict,
                                                        allocatedTraceColors=allocatedTraceColors )
                #print "Score", i, s
                return s

            newIndex = bi.min(colorIndices, key=indexScore)
            # Allocate to colorIndex:
            for g in grp:
                allocatedTraceColors[g] = newIndex

        # Make the allocation from index to colors:
        self.color_allocations = {}
        for tr in allTraces:
            self.color_allocations[tr] = self.color_cycle[ allocatedTraceColors[tr] ]
        #assert False

#l = StandardLinkages( linkages_explicit = [ (trI1,trV1,trG1), (trI2,trV2,trG2) ] )
#
##TagViewer([trI1,trV1,trG1, trI2,trV2,trG2], linkage=None)
#TagViewer([trI1,trV1,trG1, trI2,trV2,trG2], linkage=l)
#TagViewer([trI1,trV1,trG1, trI2,trV2,trG2], linkage=StandardLinkages(linkage_rules=[LinkageRuleTagRegex("Sim(\d+)")])  )


