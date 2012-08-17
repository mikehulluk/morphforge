#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -------------------------------------------------------------------------------

import numpy
from numpy import array
from numpy import linalg
from numpy.linalg import norm

from morphforge.core import LogMgr

from morphforge.morphology.visitor.visitorfactory import SVVisitorFactory


def _pca(X):
    x_mean = array(map(sum, X.T)) / len(X)
    X_ = X - x_mean
    X_t = numpy.dot(X_.T, X_) / len(X)
    (lam, vec) = linalg.eig(X_t)
    ans = zip(lam, vec.T)
    try:
        ans.sort(reverse=True)
    except:
        LogMgr.warning('Unable to sort eigenvectors')
    return ans


class PCAAxes(object):

    def __init__(self, morph):

        axes = _pca(SVVisitorFactory.array3_all_points(morph)())

        e1 = axes[0][1] / norm(axes[0][1])
        e2 = axes[1][1] / norm(axes[1][1])
        e3 = axes[2][1] / norm(axes[2][1])

        self.eigenMatrix = numpy.array((e1, e2, e3)).T
        self.invMat = linalg.inv(self.eigenMatrix)


class PointOperator(object):

    def __init__(self, operations=None):
        self.operations = (operations if operations else [])

    def __call__(self, pt):
        t = pt
        for operator in self.operations:
            t = operator(t)
        return t


class PointRotator(object):

    def __init__(self, transMatrix):
        self.transMatrix = transMatrix

    def __call__(self, pt):
        return numpy.dot(self.transMatrix, pt)


class Pointtranslater(object):

    def __init__(self, offset):
        self.offset = offset

    def __call__(self, pt):
        return pt + self.offset


class MorphologyMeanCenterer(Pointtranslater):

    def __init__(self, morph, PtSrc=None):
        PtSrc = SVVisitorFactory.array3_all_points() if PtSrc == None else PtSrc
        X = PtSrc(morph)
        offset = array(map(numpy.sum, X.T)) / len(X)
        # _get_mean(PtSrc(morph)) * -1.0
        super(MorphologyMeanCenterer, self).__init__(offset)


class MorphologyPCARotator(PointRotator):

    def __init__(self, morph):
        super(MorphologyPCARotator,
              self).__init__(PCAAxes(morph).invMat)


class MorphologyForRenderingOperator(PointOperator):

    def __init__(self, morph, usePCA=True):

        ops = [MorphologyMeanCenterer(morph)]
        if usePCA:
            ops.append(MorphologyPCARotator(morph))

        super(MorphologyForRenderingOperator, self).__init__(ops)


