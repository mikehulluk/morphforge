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

from morphforge.traces.tracetypes.tracevariabledt import TraceVariableDT

from morphforge.traces.tracetypes import TracePointBased
from morphforge.units import qty

import numpy as np

from morphforge.traces.tracetypes import TraceFixedDT
from morphforge.traces.tracetypes import TracePiecewise
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat


class TraceConverter(object):

    @classmethod
    def rebase_to_fixed_dt(cls, original_trace, dt):
        from morphforge.units.wrappers import NpPqWrappers
        time = NpPqWrappers.arange(start=original_trace.get_min_time(), stop=original_trace.get_max_time(), step=dt)
        data = original_trace.get_values(time)
        return TraceFixedDT(time, data, name=original_trace.name, comment=original_trace.comment, tags=original_trace.tags)




    @classmethod
    def reduce_to_variable_dt_trace(cls, original_trace, epsilon):
        assert isinstance(original_trace, TracePointBased)
        epsilon = qty(epsilon)

        time_units = original_trace.time_unit
        time_data = original_trace.time_pts_np

        data_units = original_trace.data_unit
        data_data = original_trace.data_pts_np


        pts = zip(time_data.tolist(), data_data.tolist())

        newpts = _simplify_points(pts, epsilon)
        (new_time, new_data) = zip(*newpts)

        new_trace = TraceVariableDT(np.array(new_time) * time_units,
                                    np.array(new_data) * data_units,
                                    name=original_trace.name,
                                    comment=original_trace.comment,
                                    tags=original_trace.tags)

        print 'Simplified from N=%d to N=%d' % (original_trace.get_n(),
                new_trace.get_n())
        return new_trace


import math

def _simplify_points (pts, tolerance):
    anchor = 0
    floater = len(pts) - 1
    stack = []
    keep = set()

    stack.append((anchor, floater))
    while stack:
        (anchor, floater) = stack.pop()

        # initialize line segment
        if pts[floater] != pts[anchor]:
            anchor_x = float(pts[floater][0] - pts[anchor][0])
            anchor_y = float(pts[floater][1] - pts[anchor][1])
            seg_len = math.sqrt(anchor_x ** 2 + anchor_y ** 2)
            # get the unit vector
            anchor_x /= seg_len
            anchor_y /= seg_len
        else:
            anchor_x = anchor_y = seg_len = 0.0

        # inner loop:
        max_dist = 0.0
        farthest = anchor + 1
        for i in range(anchor + 1, floater):
            dist_to_seg = 0.0
            # compare to anchor
            vec_x = float(pts[i][0] - pts[anchor][0])
            vec_y = float(pts[i][1] - pts[anchor][1])
            seg_len = math.sqrt(vec_x ** 2 + vec_y ** 2)
            # dot product:
            proj = vec_x * anchor_x + vec_y * anchor_y
            if proj < 0.0:
                dist_to_seg = seg_len
            else:
                # compare to floater
                vec_x = float(pts[i][0] - pts[floater][0])
                vec_y = float(pts[i][1] - pts[floater][1])
                seg_len = math.sqrt(vec_x ** 2 + vec_y ** 2)
                # dot product:
                proj = vec_x * -anchor_x + vec_y * -anchor_y
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:
                    # calculate perpendicular distance to line (pythagorean theorem):
                    dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                if max_dist < dist_to_seg:
                    max_dist = dist_to_seg
                    farthest = i

        if max_dist <= tolerance:  # use line segment
            keep.add(anchor)
            keep.add(floater)
        else:
            stack.append((anchor, farthest))
            stack.append((farthest, floater))

    keep = list(keep)
    keep.sort()
    return [pts[i] for i in keep]


class TraceApproximator(object):

    @classmethod
    def find_levels(cls, d, min_level_size=15, convolution_threshold=4):

        #x = np.arange(len(d))

        edge_filter = np.hstack((np.ones(min_level_size) * -1, np.ones(min_level_size))) / (2 * min_level_size)
        edges = np.fabs(np.convolve(d, edge_filter, mode='same'))



        edge_indices = np.where(edges > convolution_threshold)[0]

        if len(edge_indices) != 0:
            # This returns a list of numbers.
            # So, we need to find consecutive digits
            continuous_numbers_forward = (edge_indices - np.roll(edge_indices, 1)) == 1
            not_continuous_numbers_start = np.where(continuous_numbers_forward != True)[0]
            subarrays = np.split(edge_indices, not_continuous_numbers_start)

            change_points = []
            for subarray in subarrays:
                if len(subarray) == 0:
                    continue

                # Find the highest 'edge' value corresponding to the
                # to the indices in 'subarray'
                i = np.argmax(edges[subarray])
                i_max = subarray[i] #- min_level_size

                change_points.append(i_max)

            # Construct the ranges from the levels:
            ranges = []
            ranges.append((0, change_points[0]))
            for cp_i in range(len(change_points) - 1):
                ranges.append((change_points[cp_i], change_points[cp_i + 1]))
            ranges.append((change_points[-1], len(d)-1))
        else:
            ranges = [(0, len(d)-1)]

        return ranges




    @classmethod
    def fit_piecewise_linear_trace(cls, tr):
        ranges = TraceApproximator.find_levels(tr.data_pts_np)

        pieces = []
        for r0, r1 in ranges:
            x = np.mean(tr.data_pts[r0:r1])
            p = TracePieceFunctionFlat(time_window=(tr.time_pts[r0], tr.time_pts[r1]), x=x)
            pieces.append(p)

        tr = TracePiecewise(pieces, name=tr.name, comment=tr.comment, tags=tr.tags)
        return tr

