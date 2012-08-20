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
from morphforge.traces.eventset import EventSet


class DBScan(object):

    @classmethod
    def query_region(cls, p, eps, pts):
        nr_indices = np.nonzero(np.fabs(pts - p) < eps)[0]
        return set(nr_indices)

    @classmethod
    def cluster_points(cls, pts, eps, min_pts):
        pts = np.array(pts)
        visited_indices = [False] * np.zeros(len(pts))
        noise = []
        clusters = []

        for (i, pt) in enumerate(pts):
            if visited_indices[i]:
                continue

            visited_indices[i] = 1

            n_points = cls.query_region(p=pt, eps=eps, pts=pts)

            if len(n_points) < min_pts:
                noise.append(i)
            else:
                new_cluster = set()
                cls.expand_cluster(pt_index=i, npoints=n_points, cluster=new_cluster, eps=eps, pts=pts, min_pts=min_pts,  visited_indices=visited_indices, clusters=clusters)
                clusters.append(new_cluster)

        return (clusters, noise)

    @classmethod
    def expand_cluster(cls, pt_index, npoints, cluster, pts, eps, visited_indices,  min_pts, clusters):

        cluster.add(pt_index)

        iter_n = list(npoints)
        while iter_n:
            pdash_index = iter_n.pop()
            if not visited_indices[pdash_index]:

                visited_indices[pdash_index] = 1
                n_dash = cls.query_region(p=pts[pdash_index], eps=eps, pts=pts)

                if len(n_dash) >= min_pts:
                    for n in n_dash:
                        iter_n.append(n)

                pt_in_clusters = [True for c in clusters if pdash_index in c]
                if not pt_in_clusters:
                    cluster.add(pdash_index)


    @classmethod
    def cluster_spike_times(cls, event_set, eps, min_pts=5):
        eps = float(eps.rescale('ms').magnitude)

        data = [float(ev.get_time().rescale('ms')) for ev in event_set]
        (clusters, noise) = DBScan.cluster_points(pts=np.array(data), eps=eps, min_pts=min_pts)

        # Create new eventsets for each cluster
        new_eventsets = []
        for cluster in clusters:
            e = EventSet()
            for c in cluster:
                e.add_event(event_set[c])
            new_eventsets.append(e)

        # Create a new EventSet for the noise points:
        noise_event_set = EventSet(events=[event_set[i] for i in noise])

        return new_eventsets, noise_event_set


    @classmethod
    def calculate_mean_frequency(cls, cluster_sets):


        mean_times = [np.mean([t.rescale('ms') for t in c.times]) for c in cluster_sets if len(c) != 0]
        mean_times = np.array([mt for mt in mean_times if mt > 200])

        np.sort(mean_times)
        mean_times.sort()
        print mean_times

        isi = np.diff(mean_times)
        freq = 1000.0 / isi
        mean_freq = np.mean(freq)

        return mean_freq


