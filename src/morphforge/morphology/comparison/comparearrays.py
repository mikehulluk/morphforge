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

# This class looks internally at objects, 
# so we relax the access restrictions:
# pylint: disable=W0212

class MorphArrayComparison(object):

    @classmethod
    def are_same(cls, m1, m2, max_node_distance=0.01, max_radius_distance=None):
        from scipy.spatial.distance import pdist

        max_radius_distance = max_radius_distance if max_radius_distance is not None else max_node_distance

        m1 = m1.to_array()
        m2 = m2.to_array()

        if len(m1) != len(m2):
            return False  # , {'reason', 'different length morphologies'}

        # Check that the shortest distance between 2 points in m1 and m2 are
        # greater that 'max_node_distance':
        dist1 = np.min(pdist(m1._vertices[:, 0:3], 'euclidean'))
        if dist1 < max_node_distance:
            return False  # , {'reason':'m1 has nodes that are too close together'}

        dist2 = np.min(pdist(m2._vertices[:, 0:3], 'euclidean'))
        if dist2 < max_node_distance:
            return False  # , {'reason':'m2 has nodes that are too close together'}

        #print 'dist1, dist2', dist1, dist2

        # Create a map between indices in each morphology,
        # based on positions:
        (index_map, max_dist) = cls.get_id_mapping_from_positions(m1, m2)
        if index_map is None:
            return False
        if max_dist > max_node_distance:
            return False

        # Check the connectivity:
        m2_connectivity = set([tuple(t) for t in m2._connectivity.tolist()])
        for (i1, j1) in m1._connectivity:
            i2 = index_map[i1]
            j2 = index_map[j1]
            if not (i2, j2) in m2_connectivity:
                return False 


        # Check the radii:
        for (i1, i2) in index_map.iteritems():
            if not np.fabs(m1._vertices[i1, 3] - m2._vertices[i2, 3]) < max_radius_distance:
                return False

        # Check the region types:
        for (index, (i1, j1)) in enumerate(m1._connectivity):
            i2 = index_map[i1]
            j2 = index_map[j1]
            c2 = m2.index_of_connection(i2, j2)

            if m1._section_types[index] != m2._section_types[c2]:
                return False  # , {'max_dist':max_dist, 'reason':'the section types were different'}

        return True

    @classmethod
    def get_id_mapping_from_positions(cls, m1, m2):

        import scipy.spatial
        kd_tree = scipy.spatial.KDTree(m2._vertices[:, 0:3])

        id_map = {}
        max_dist = 0
        for (vi, v) in enumerate(m1._vertices[:, 0:3]):
            (dist, nearest_neighbour) = kd_tree.query(v)

            if vi in id_map:
                return None

            id_map[vi] = nearest_neighbour
            max_dist = max(max_dist, dist)

        return (id_map, max_dist)


