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

#print 
import numpy as np
#import numpy.linalg
#from numpy import array
#from numpy import linalg

from morphforge.core import LogMgr

from morphforge.morphology.visitor.visitorfactory import SectionVistorFactory


def _pca(X):

    # Refactored out 'map' in August 2012
    # x_mean = array(map(sum, X.T)) / len(X)
    x_mean = np.array([sum(col) for col in X.T])/len(X)

    x_ = X - x_mean
    x_t = np.dot(x_.T, x_) / len(X)
    (lam, vec) = linalg.eig(x_t)
    ans = zip(lam, vec.T)
    print ans
    try:
        ans.sort(reverse=True, key=lambda t: t[0])
    except Exception, e:
        print e
        assert False, 'What is the exception raised?!'
        LogMgr.warning('Unable to sort eigenvectors')
    return ans


class PCAAxes(object):

    def __init__(self, morph):
        from numpy.linalg import norm

        axes = _pca(SectionVistorFactory.array3_all_points(morph)())

        eigenvec1 = axes[0][1] / norm(axes[0][1])
        eigenvec2 = axes[1][1] / norm(axes[1][1])
        eigenvec3 = axes[2][1] / norm(axes[2][1])

        self.eigen_matrix = np.array((eigenvec1, eigenvec2, eigenvec3)).T
        self.inv_mat = linalg.inv(self.eigen_matrix)


class PointOperator(object):

    def __init__(self, operations=None):
        self.operations = (operations if operations else [])

    def __call__(self, pt):
        result = pt
        for operator in self.operations:
            result = operator(result)
        return result


class PointRotator(object):

    def __init__(self, transMatrix):
        self.transMatrix = transMatrix

    def __call__(self, pt):
        return np.dot(self.transMatrix, pt)


class Pointtranslater(object):

    def __init__(self, offset):
        self.offset = offset

    def __call__(self, pt):
        return pt + self.offset


class MorphologyMeanCenterer(Pointtranslater):

    def __init__(self, morph, PtSrc=None):
        PtSrc = SectionVistorFactory.array3_all_points() if PtSrc == None else PtSrc
        X = PtSrc(morph)
        
        # Refactored out 'map' in August 2012
        offset = np.array([sum(col) for col in X.T]) / len(X)

        # _get_mean(PtSrc(morph)) * -1.0
        super(MorphologyMeanCenterer, self).__init__(offset)


class MorphologyPCARotator(PointRotator):

    def __init__(self, morph):
        super(MorphologyPCARotator,
              self).__init__(PCAAxes(morph).inv_mat)


class MorphologyForRenderingOperator(PointOperator):

    def __init__(self, morph, usePCA=True):

        ops = [MorphologyMeanCenterer(morph)]
        if usePCA:
            ops.append(MorphologyPCARotator(morph))

        super(MorphologyForRenderingOperator, self).__init__(ops)


