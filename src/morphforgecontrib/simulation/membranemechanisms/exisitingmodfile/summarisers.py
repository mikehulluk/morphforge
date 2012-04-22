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
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforge.constants.standardtags import StandardTags
from morphforge.core.units import unit
from morphforge.simulation.core.biophysics.membranemechanism import MembraneMechanism
from mhlibs.eqnset.equationset.eqnset_loader import EquationSetLoader
from morphforge.constants.stdrecordables import StdRec
from morphforge.simulation.neuron.biophysics.mm_neuron import MM_Neuron_Base
from Cheetah.Template import Template
#from morphforge.indev.eqnset.neuron_mapping import NeuronCurrent
from mhlibs.eqnset.equationset.nmodl_writer import NMODLWriter
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import  * 
#from morphforge.simulation.neuron.objects.
import copy

import quantities as pq




import numpy as np


class EqnSetPlotter():
    V = np.linspace(-80.,50.,num=1000) / 1000.
    
    
    def __init__(self, chlCls):
        self.eqnset = chlCls.eqnset
        
        
    def getPlotAgainstV(self, alias):
        assert False
        
    def plotstd(self):
        from morphforge.indev.eqnset.equationset.visitor_callablebuilder import CallableVisitorBuilder 
        print self.eqnset.alias_map.keys()
        
        import quantities as pq
        V = np.linspace(-80, 80) * pq.milli * pq.V
        
        m_alpha = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['alpha_m'] ) ( {'V': V} )
        m_beta = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['beta_m'] ) ( {'V': V} )
        m_inf = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['minf'] ) ( {'V': V} )
        m_tau = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['mtau'] ) ( {'V': V} )
        
        h_alpha = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['alpha_h'] ) ( {'V': V} )
        h_beta = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['beta_h'] ) ( {'V': V} )
        h_inf = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['hinf'] ) ( {'V': V} )
        h_tau = CallableVisitorBuilder(self.eqnset).build_callable(['V'], self.eqnset.alias_map['htau'] ) ( {'V': V} )
        
        
        
        from morphforge.core.quantities_plot import QuantitiesFigure  
        q = QuantitiesFigure()
        ax = q.add_subplot(311)
        ax.plot(V, m_alpha )
        ax.plot(V, m_beta )
        ax.legend()
        
        ax = q.add_subplot(312, ylabel="Steady\nState")
        ax.plot(V, m_inf, label='m' )
        ax.plot(V, h_inf, label='h' )
        ax.legend()
        
        ax = q.add_subplot(313, yUnit='ms', ylabel='Time Constant' )
        ax.plot(V, m_tau, label='m' )
        ax.plot(V, h_tau, label='h' )
        ax.legend()
        
        
        #import pylab as pl
        #pl.show()
        
        #assert False
        

