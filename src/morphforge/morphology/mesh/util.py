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


def norm_vec(v):
    return v / np.sqrt(np.dot(v, v))


def get_normal_vectors(vec):
    vec_norm = vec / np.sqrt(np.dot(vec, vec))
    vec_norm = norm_vec(vec)

    # Decided which vector to use as a basis to find the normals
    # We want something that is not too parallel...
    normc1 = np.array([1.0, 0.0, 0.0])
    normc2 = np.array([0.0, 1.0, 0.0])
    normc = (normc1 if np.dot(vec_norm, normc1) < 0.4 else normc2)

    perp1 = norm_vec(normc - np.dot(normc, vec))
    perp2 = norm_vec(np.cross(vec, perp1))

    return (perp1, perp2)


def get_point_circle_about(pt, normal, radius, n):
    (perp1, perp2) = get_normal_vectors(normal)
    angle_step = 2 * np.pi / n
    angles = [i * angle_step for i in range(0, n)]
    pts = [pt + radius * (perp1 * np.sin(angle) + perp2 * np.cos(angle))
           for angle in angles]
    return np.array(pts)


def find_closest_points(pts1, pts2):

    def dist_sqd_between_indices(i1, i2):
        joining = pts1[i1] - pts2[i2]
        return np.dot(joining, joining)

    min_dist = dist_sqd_between_indices(0, 0)
    min_inds = (0, 0)

    for i in range(0, len(pts1)):
        for j in range(0, len(pts2)):
            d = dist_sqd_between_indices(i, j)
            if d < min_dist:
                min_dist = d
                min_inds = (i, j)
    return min_inds


def get_best_joining_offset(pts1, pts2):

    assert len(pts1) == len(pts2)
    n = len(pts1)

    bestoffset = 0
    bestlength = None

    for offset in range(n):

        joiningvectors = []
        for i in range(n):
            jv = pts1[i] - pts2[(i + offset) % n]
            joiningvectors.append(jv)

        s = np.sum(joiningvectors)

        l = np.dot(s, s)
        if l > bestlength:
            bestlength = l
            bestoffset = 0

    return (0, bestoffset)


