#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

#from reportlab.pdfgen import canvas
#from reportlab.platypus import *
#import itertools
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.lib import colors
#iimport os
#i#from reportlab.lib.pagesizes import A4

#from ..stdlimits import StdLimits
#import morphforge


#from morphforge.core.quantities_plot import QuantitiesFigure

import numpy as np

import morphforge.core.quantities as pq
#from morphforge.core import unit

class AlphaBetaCalculator(object):

    @classmethod
    def calc_alpha_beta(cls, V, ab ):
        v = V.rescale("mV").magnitude
        alphabeta = (ab[0] + ab[1] * v) / (ab[2] + np.exp((ab[3] + v) / ab[4]))
        alphabeta = alphabeta * (pq.J/pq.J)
        return alphabeta


    #@classmethod
    #def getAlphaBeta(cls, V, alpha, beta):
    #    alpha = cls.calc_alpha_beta(V,alpha)
    #    beta =  cls.calc_alpha_beta(V,beta)
    #    return alpha,beta







#class AlphaBetaBetaCalculator(object):
#
#    @classmethod
#    def calc_alpha_beta(cls, V, ab ):
#        v = V.rescale("mV").magnitude
#        alphabeta = (ab[0] + ab[1] * v) / (ab[2] + np.exp((ab[3] + v) / ab[4]))
#        alphabeta = alphabeta * pq.dimensionless
#        return alphabeta
#
#
#    @classmethod
#    def getAlphaBetaBeta(cls, V, alpha, beta1, beta2, threshold):
#        alpha = cls.calc_alpha_beta(V,alpha)
#        beta1 = cls.calc_alpha_beta(V,beta1)
#        beta2 = cls.calc_alpha_beta(V,beta2)
#
#        betaIndices1 = np.nonzero( V <  threshold )
#        betaIndices2 = np.nonzero( V >= threshold )
#
#        beta = np.hstack( [beta1[betaIndices1],beta2[betaIndices2] ] )
#
#        return alpha, beta










class InfTauCalculator(object):
    @classmethod
    def alpha_beta_to_inf_tau(cls,alpha,beta):
        inf = alpha/(alpha+beta)
        tau = 1.0/(alpha+beta) * pq.milli * pq.second
        return inf,tau


    @classmethod
    def evaluate_inf_tau_for_v(cls, (alphaParams, betaParams), V):
        alpha, beta = AlphaBetaCalculator.getAlphaBeta(V, alphaParams,betaParams)
        inf, tau = InfTauCalculator.alpha_beta_to_inf_tau(alpha, beta)
        return inf,tau



class ReportLabTools(object):

    @classmethod
    def build_alpha_beta_table(cls, elements, reportlabconfig, title, params ):

        from reportlab.platypus import Paragraph, Table
        elements.append( Paragraph(title,reportlabconfig.styles['Heading4']) )
        print params
        print
        alphaParams = "%2.2f %2.2f %2.2f %2.2f %2.2f"%tuple(params)
        alpha_table_data = [ ["A","B","C","D","E"], alphaParams.split()  ]
        elements.append( Table(alpha_table_data, style=reportlabconfig.defaultTableStyle) )

