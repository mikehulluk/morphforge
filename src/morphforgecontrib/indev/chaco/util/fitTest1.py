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
import pylab as pl
from pylab import *
from scipy import *
from scipy import optimize

#v = np.array(v)
#m_inf = np.array(m_inf)
#tau = np.array(tau)


#alpha = m_inf/tau
#beta = (1-tau*alpha)/(tau)



#v= [-100.,    -82.22,  -64.44,  -46.67,  -28.89,  -11.11,    6.67,   24.44,   42.22, 60., ]
#alpha = [0.12,  0.19,  0.28,  0.36,  0.44,  0.51,  0.59,  0.67,  0.74,  0.82]
#beta = [0.54,  0.36,  0.24,  0.15,  0.08,  0.04,  0.02,  0.01,  0.01,  0. ]

v= [-100.,    -82.22,  -64.44,  -46.67,  -28.89,  -11.11,    6.67,   24.44,   42.22,   60. ]
alpha= [0.,    0.,    0.02,  0.11,  0.31,  0.57,  0.82,  1.13,  1.42,  1.7, ]
beta= [3.95,  2.36,  1.42,  0.85,  0.43,  0.25,  0.18,  0.11,  0.07,  0.04]
tau= [0.25,  0.42,  0.69,  1.05,  1.35,  1.21,  1.,    0.81,  0.67,  0.57]
inf= [0.,    0.,    0.02,  0.11,  0.42,  0.69,  0.82,  0.91,  0.95,  0.98]


v= [-100. ,   -82.22,  -64.44,  -46.67,  -28.89,  -11.11,    6.67,   24.44,   42.22, 60. ]
alpha= [0.,    0.,    0.04,  0.14,  0.31,  0.5,   0.73,  1.06,  1.34,  1.7, ]
beta= [4.34,  2.36,  1.42,  0.7,   0.37,  0.22,  0.17,  0.11,  0.06,  0.04]
#Tau: [0.23  0.42  0.68  1.19  1.46  1.38  1.11  0.86  0.71  0.57]
#Inf: [0.    0.    0.03  0.16  0.46  0.69  0.81  0.91  0.95  0.98]


Index= [-100.,    -82.22, -64.44, -46.67, -28.89, -11.11,   6.67,  24.44,  42.22, 60. ]
Alpha= [0.,    0.,    0.04, 0.2,  0.68, 1.95, 3.11, 4.69, 6.36, 8. ]
Beta= [4.08, 3.98, 3.94, 3.79, 2.98, 1.05, 0.32, 0.09, 0.,    0.03]



Index= [-100.,    -82.22, -64.44, -46.67, -28.89, -11.11,   6.67,  24.44,  42.22, 60. ]
Alpha= [ 9.61e+00,  2.53e+00,  9.44e-01,  3.43e-01,  5.89e-02,  1.24e-02, 1.51e-03,  0.00e+00,  0.00e+00,  0.00e+00]
Beta= [0.,    0.,    0.02, 0.04, 0.13, 0.28, 0.69, 2.73, 3.9,  4. ]


Index= [-100.,    -82.22, -64.44, -46.67, -28.89, -11.11,   6.67,  24.44,  42.22, 60. ]
Alpha= [ 2.85e+00,  1.67e+00,  9.44e-01,  3.43e-01,  8.38e-02,  1.48e-02, -1.18e-03,  0.00e+00,  0.00e+00,  0.00e+00]
Beta= [0.,    0.,    0.02, 0.04, 0.13, 0.28, 0.69, 2.73, 3.9,  4. ]



Index = [-100.,   -82.22, -64.44, -46.67, -28.89, -11.11,   6.67,  24.44,  42.22, 60., ]
Alpha = [ 8.95e+00,  1.85e+00,  9.58e-01,  4.45e-01,  1.01e-01,  2.02e-02, 2.02e-02,  6.75e-03,  6.75e-03,  3.33e-16]
Beta = [0.,   0.,   0.,   0.01, 0.11, 0.32, 0.73, 2.75, 3.67, 4., ]


Index= [-100.,   -82.22, -64.44, -46.67, -28.89, -11.11,   6.67,  24.44,  42.22, 60., ]
Alpha= [0.,   0.,   0.04, 0.2,  0.72, 2.24, 5.24, 7.63, 8.33, 8.33]
Beta= [3.85, 3.85, 3.81, 3.8,  3.44, 2.31, 0.64, 0.06, 0.,   0., ]

inf= """
-100.00 1.00
-82.22 1.00
-64.44 1.00
-46.67 0.98
-28.89 0.49
-11.11 0.06
6.67 0.03
24.44 0.00
42.22 0.00
60.00 0.00
"""
tau = """
-100.00 0.11
-82.22 0.53
-64.44 1.04
-46.67 2.21
-28.89 4.82
-11.11 2.96
6.67 1.33
24.44 0.36
42.22 0.27
60.00 0.25
"""

inf = [float(i) for i in inf.split()]
tau = [float(i) for i in tau.split()]
assert len(inf) == len(tau) == 20

v = inf[0::2]
inf = inf[1::2]
tau = tau[1::2]
Alpha = np.array(inf)/np.array(tau)
Beta = (1-np.array(tau) * Alpha) /np.array(tau)






v = Index
alpha = Alpha
beta = Beta

v = np.array(v)
alpha = np.array(alpha)
beta = np.array(beta)



m  = v > -80
v =v[m]
alpha=alpha[m]
beta=beta[m]



v_fit = np.linspace(-100, 60, 100)
#print alpha,
#print beta
#assert False

def fitfunc(p, x):
    #return (p[0])/(p[2] + np.exp((p[3]+x)/p[4]))
    return (p[0])/(p[2] + np.exp((p[3]+x)/p[4]))

    return (p[0] + p[1]*x)/(p[2] + np.exp((p[3]+x)/p[4]))

def errfunc(p, x, y):
    dist = fitfunc(p, x) - y

    #print fitfunc(p, v_fit)
    if np.isnan(fitfunc(p, v_fit)).any():
        assert False
        return 1000
    r = np.dot(dist.T,  dist)
    return r


# Distance to the target function
#p0_alpha = [0.095, 0.000, 1.0, 1.0, -8]
#p0_alpha = [0.461973318, 0.00820458521, 4.59367292, -4.20812882, -11.9678988, ]
p0_alpha=[5.06, 0.07, 5.12, -18.4, -25.42]
p0_alpha = [ 1.23807353e-01,   1.63897392e-03,  -1.05356548e-01,   2.98171398e+01, 2.02269962e+01]
p0_alpha = [0.18881081, -0.00578191,  0.05032903,  0.00791992,  3.19731029]
p0_alpha = [1.26585951e-05,  -7.64869304e-03,   1.00209483e-06,   1.29657042e-02, 6.77722948e+00]
p0_alpha = [1.22452064e-02,  -1.62282471e-03,  -1.41915248e-03,   2.22988192e+00,   2.95280879e+01]

p1_alpha = optimize.fmin(errfunc, np.array(p0_alpha), args=(v, alpha))
print 'P1-Alpha', p1_alpha


p0_beta = [ 0.2,   0.003,  -8.95334802e-02, -1.0,   25]
#p0_beta = [0.12, 0.0, 2.0, 30, 9.0]
p0_beta = [ 1.23807353e-01,   1.63897392e-03,  -1.05356548e-01,   2.98171398e+01, 2.02269962e+01]
p0_beta=[5.06, 0.07, 5.12, -18.4, -25.42]
p0_beta=[5.06, 0.00, 1, 0, 1]
p0_beta = [0.18881081, -0.00578191,  0.05032903,  0.00791992,  3.19731029]
p0_beta = [ 4.69173146e-01,   2.95636835e-03,   1.17652953e-01,   4.80687239e-02, -8.43859689e+00]

p1_beta = optimize.fmin(errfunc, np.array(p0_beta), args=(v, beta))
print 'P1-Beta', p1_beta



v_fit = np.linspace(-100, 60, 100)
alpha_fit = fitfunc(p1_alpha, v_fit)
beta_fit = fitfunc(p1_beta, v_fit)

pl.plot(v, alpha, 'r', label='Orig')
pl.plot(v_fit, alpha_fit, 'b', label='Fit')
pl.legend()

pl.figure()
pl.plot(v, beta, 'r', label='Orig')
pl.plot(v_fit, beta_fit, 'b', label='Fit')
pl.legend()
pl.show()
#pl.show()


