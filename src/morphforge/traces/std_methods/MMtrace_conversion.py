#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.traces.tracetypes.traceVariableDT import Trace_VariableDT

from morphforge.traces.tracetypes import Trace_PointBased
from morphforge.core.quantities.fromcore import unit

import numpy as np

from morphforge.traces.tracetypes import Trace_FixedDT
from morphforge.traces.tracetypes import Trace_Piecewise
from morphforge.traces.tracetypes.tracePiecewise import TracePieceFunctionFlat

class TraceConverter(object):

    @classmethod
    def rebase_to_fixed_dt(cls, original_trace, dt):
        from morphforge.core.quantities.wrappers import NpPqWrappers
        time = NpPqWrappers.arange(start=original_trace.get_min_time(), stop=original_trace.get_max_time(), step=dt)
        data = original_trace.get_values(time)
        return Trace_FixedDT(time, data, name=original_trace.name, comment=original_trace.comment, tags=original_trace.tags)




    @classmethod
    def reduce_to_variable_dt_trace(cls, original_trace, epsilon):
        assert isinstance(original_trace, Trace_PointBased)
        epsilon = unit(epsilon)


        time_units = original_trace._time.units
        time_data = original_trace._time.magnitude

        data_units = original_trace._data.units
        data_data = original_trace._data.magnitude

        ep = epsilon

        pts = zip(time_data.tolist(), data_data.tolist())


        newpts = _simplify_points(pts, ep)
        new_time, new_data = zip(*newpts)

        newTrace = Trace_VariableDT(np.array(new_time) * time_units, np.array(new_data) * data_units, name=original_trace.name, comment=original_trace.comment, tags=original_trace.tags)

        print 'Simplified from N=%d to N=%d' % (original_trace.get_n(), newTrace.get_n())
        return newTrace







import math

def _simplify_points (pts, tolerance):
    anchor = 0
    floater = len(pts) - 1
    stack = []
    keep = set()

    stack.append((anchor, floater))
    while stack:
        anchor, floater = stack.pop()

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
            vecX = float(pts[i][0] - pts[anchor][0])
            vecY = float(pts[i][1] - pts[anchor][1])
            seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
            # dot product:
            proj = vecX * anchor_x + vecY * anchor_y
            if proj < 0.0:
                dist_to_seg = seg_len
            else:
                # compare to floater
                vecX = float(pts[i][0] - pts[floater][0])
                vecY = float(pts[i][1] - pts[floater][1])
                seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
                # dot product:
                proj = vecX * (-anchor_x) + vecY * (-anchor_y)
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:  # calculate perpendicular distance to line (pythagorean theorem):
                    dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                if max_dist < dist_to_seg:
                    max_dist = dist_to_seg
                    farthest = i

        if max_dist <= tolerance: # use line segment
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


       x = np.arange(len(d))

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
           for s in subarrays:
               if len(s) == 0:
                   continue

               # Find the highest 'edge' value corresponding to the
               # to the indices in 's'
               i = np.argmax(edges[s])
               iMax = s[i] #- min_level_size

               change_points.append(iMax)

           # Construct the ranges from the levels:
           ranges = []
           ranges.append((0, change_points[0]))
           for cpI in range(len(change_points) - 1):
               ranges.append((change_points[cpI], change_points[cpI + 1]))
           ranges.append((change_points[-1], len(d)-1))
       else:
           ranges = [ (0, len(d)-1) ]

       return ranges




   @classmethod
   def fit_piecewise_linear_trace( cls, tr):
         d = tr._data.magnitude

         ranges = TraceApproximator.find_levels(d)

         pieces = []
         for r0,r1 in ranges:
             #print r0,r1
             x = np.mean( tr._data[r0:r1] )
             p = TracePieceFunctionFlat( time_window=(tr._time[r0],tr._time[r1]), x=x,)
             pieces.append(p)

         tr = Trace_Piecewise(pieces, name=tr.name, comment=tr.comment, tags=tr.tags)
         return tr

