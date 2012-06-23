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
from morphforge.stdimports import *
from modelling.rbmodelling2.modelconstants import ChlType, Model, CellType
from scipy.interpolate import interp1d

naFunctor = ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12Interpolated, celltype=CellType.dIN, channeltype=ChlType.Na)
kfFunctor = ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12Interpolated, celltype=CellType.dIN, channeltype=ChlType.Kf)
ksFunctor = ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12Interpolated, celltype=CellType.dIN, channeltype=ChlType.Ks)
lkFunctor = ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12Interpolated, celltype=CellType.dIN, channeltype=ChlType.Lk)
#caFunctor = ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12Interpolated, celltype=CellType.dIN, channeltype=ChlType.Ca)

env = NeuronSimulationEnvironment()
naChl = naFunctor(env)
kfChl = kfFunctor(env)
ksChl = ksFunctor(env)
lkChl = lkFunctor(env)



def interpolate_inf(chl, state, V):
    params = chl.statevars_new[state]
    return interp1d(x=params.V, y=params.inf)(V)


def m_inf(V):
    return interpolate_inf(naChl, 'm',V)

def h_inf(V):
    return interpolate_inf(naChl, 'h',V)

def kf_inf(V):
    return interpolate_inf(kfChl, 'kf',V)

def ks_inf(V):
    return interpolate_inf(ksChl, 'ks',V)

import numpy as np
v = np.linspace(-75,35,100)

minf = m_inf(v)


SA = unit('1000:um2')

iNa = ( naChl.conductance * SA * m_inf(v)*m_inf(v)*m_inf(v)*h_inf(v) * ( v*mV - naChl.reversalpotential) ).rescale('pA').magnitude
iKf = ( kfChl.conductance * SA * kf_inf(v)*kf_inf(v)*kf_inf(v)*kf_inf(v) * ( v*mV - kfChl.reversalpotential) ).rescale('pA').magnitude
iKs = ( ksChl.conductance * SA * ks_inf(v)*ks_inf(v) * ( v*mV - ksChl.reversalpotential) ).rescale('pA').magnitude
iLk = ( lkChl.conductance * SA * ( v*mV - lkChl.reversalpotential) ).rescale('pA').magnitude


sNa =  m_inf(v)*m_inf(v)*m_inf(v)*h_inf(v)
sKf =  kf_inf(v)*kf_inf(v)*kf_inf(v)*kf_inf(v)
sKs =  ks_inf(v)*ks_inf(v)


def get_nCurve(iExt):
    n4 = ((iNa + iLk + iKf) + iExt) / ( ksChl.conductance * SA * (v*mV-ksChl.reversalpotential) ).rescale('pA').magnitude
    n = np.power(n4,0.5)
    return n


def dVdt(iExt, n):
    iNa + iKf + iLk




#pylab.plot(v,n4, label='n4')
pylab.plot(v,get_nCurve(0), label='n, Iext=0')
pylab.plot(v,get_nCurve(100), label='n, Iext=100')
pylab.plot(v,get_nCurve(150), label='n, Iext=150')
pylab.plot(v,get_nCurve(200), label='n, Iext=200')
pylab.plot(v, ks_inf(v), label='ks_inf')
pylab.legend()

#pylab.show()



#import sys
#sys.exit(0)

pylab.figure()
pylab.plot(v,sNa, label='Na-inf')
pylab.plot(v,sKf, label='Kf-inf')
pylab.plot(v,sKs, label='Ks-inf')
pylab.legend()


pylab.figure()
pylab.plot(v,iNa, label='Na-i')
pylab.plot(v,iKf, label='Kf-i')
pylab.plot(v,iKs, label='Ks-i')
pylab.plot(v,iLk, label='Lk-i')
pylab.legend()
pylab.show()






