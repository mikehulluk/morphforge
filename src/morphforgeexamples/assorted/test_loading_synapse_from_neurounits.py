



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
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
#from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_neuron import MM_Neuron_NeuroUnits_GenRecord
#from neurounits.neurounitparser import NeuroUnitParser
#from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel
#from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.neuron import MM_Neuron_SimulatorSpecificChannel
#from neurounits.tools.nmodl import WriteToNMODL
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism
from morphforge.constants.stdrecordables import StdRec

from neurounits import NeuroUnitParser

from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_TimeList
from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_VoltageThreshold
from morphforgecontrib.simulation.synapses_neurounit import NeuroUnitEqnsetPostSynaptic


from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_core import NeuroML_Via_XSL_Channel

import random as R

from morphforge.traces.eventset import Event








def simulate_chls_on_neuron():
    # Create the environment:
    env = NeuronSimulationEnvironment()

    # Create the simulation:
    mySim = env.Simulation()

    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    myCell1 = mySim.createCell(name="Cell1", morphology=m1)
    apply_mechanism_everywhere_uniform( myCell1, env.MembraneMechanism(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA" ) ) 
    apply_passive_everywhere_uniform(myCell1, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )

    m2 = MorphologyTree.fromDictionary(morphDict1)
    myCell2 = mySim.createCell(name="Cell2", morphology=m2)
    apply_mechanism_everywhere_uniform( myCell2, env.MembraneMechanism(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA" ) ) 
    apply_passive_everywhere_uniform(myCell2, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )

    # Get a location on the cell:
    somaLoc1 = myCell1.getLocation("soma")
    somaLoc2 = myCell2.getLocation("soma")


    eqnsetfile = "/home/michael/hw_to_come/libs/NeuroUnits/src/test_data/eqnsets/syn_simple.eqn"
    syn = mySim.createSynapse(
            presynaptic_mech =  env.PreSynapticMechanism(
                                     PreSynapticMech_TimeList,
                                     timeList =   (100,105,110,112,115, 115,115) * pq.ms ,
                                     weight = unit("1:nS")),
            postsynaptic_mech = env.PostSynapticMechanism(
                                     NeuroUnitEqnsetPostSynaptic,
                                     name = "mYName1",
                                     eqnset = NeuroUnitParser.EqnSet(open(eqnsetfile).read()),
                                     celllocation = somaLoc1
                                     )
            )
    
    syn = mySim.createSynapse(
            presynaptic_mech =  env.PreSynapticMechanism(
                                     PreSynapticMech_VoltageThreshold,
                                     celllocation=somaLoc1,
                                     voltageThreshold=unit("0:mV"),
                                     delay=unit('1:ms'),
                                     weight = unit("1:nS")),
            postsynaptic_mech = env.PostSynapticMechanism(
                                     NeuroUnitEqnsetPostSynaptic,
                                     name = "mYName1",
                                     eqnset = NeuroUnitParser.EqnSet(open(eqnsetfile).read()),
                                     celllocation = somaLoc2
                                     )
            )

    # Create the stimulus and record the injected current:
    #cc = mySim.createCurrentClamp( name="Stim1", amp=unit("100:pA"), dur=unit("100:ms"), delay=unit("100:ms") * R.uniform(0.95,1.0), celllocation=somaLoc)


    # Define what to record:
    mySim.record( myCell1, what=StdRec.MembraneVoltage, name="SomaVoltage1", location = somaLoc1 )
    mySim.record( myCell2, what=StdRec.MembraneVoltage, name="SomaVoltage2", location = somaLoc2 )


    # Run the simulation
    results = mySim.Run()
    return results









#
#resultsE = simulate_chls_on_neuron( apply_hh_chls_neurounits_direct )
#TagViewer([resultsE], timeranges=[(95, 200)*pq.ms], show=True )
#
#import sys
#sys.exit(0)



#'resultsA =None
#'resultsB =None
#'resultsC =None
#'resultsD =None
#'resultsE =None
#'

resultsB = simulate_chls_on_neuron()
TagViewer(resultsB, timeranges=[(95, 200)*pq.ms], show=True )
#
#trs = [resultsA,resultsB,resultsC,resultsD,resultsE]
#trs = [tr for tr in trs if tr is not None]

import sys
sys.exit(0)



import pylab





resultsC = simulate_chls_on_neuron( apply_hh_chls_neuroml_neurounits )
resultsD = simulate_chls_on_neuron( apply_hh_chls_neuroml_xsl )
resultsE = simulate_chls_on_neuron( apply_hh_chls_neurounits_direct )


TagViewer([resultsC,resultsD,resultsE], timeranges=[(95, 200)*pq.ms], show=True )
#TagViewer([resultsC], timeranges=[(95, 200)*pq.ms], show=True )



for v in vars:
    ax = pylab.figure().add_subplot(111)
    tr = resultsC.getTrace(v)
    ax.plot( tr._time.magnitude, tr._data.magnitude, label=v )
    ax.legend()
#pylab.show()


#import sys
#sys.exit(1)



TagViewer([resultsC,resultsD], timeranges=[(95, 200)*pq.ms], show=True )




import sys
sys.exit(1)


resultsA = simulate_chls_on_neuron( apply_hh_chls_morphforge_format )
resultsB = simulate_chls_on_neuron( apply_hh_chls_NEURON_builtin )
# Display the results:
TagViewer([resultsA,resultsB,resultsC], timeranges=[(95, 200)*pq.ms], show=True )


