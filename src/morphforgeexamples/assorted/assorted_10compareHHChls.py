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

"""Comparing simulations: the Hodgkin-Huxley '52 channels

This simulation compares the different ways of implementing the Hodgkin-Huxley channels;
we check that the Hodgkin-Huxley channels built-in to NEURON produce the same results as
when we create these channels with parameters as an MM_AlphaBetaChannel.

In you are not familiar with python, then this is an example of the one of 
the advantages of the laanguage: functions are objects!

In "test_neuron", we create a neuron morphology, but put the code to add the channels
in a different function. This makes it easy to try out different channel types and
distributions easily and quickly.
 
"""

 

from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel


def apply_hh_chls_morphforge_format(env, myCell):
    
    leakChannels = env.MembraneMechanism( 
                             MM_LeakChannel, 
                             name="LkChl", 
                             conductance=unit("0.3:mS/cm2"), 
                             reversalpotential=unit("-54.3:mV"),
                             mechanism_id = 'HULL12_DIN_LK_ID'
                            )
    
    sodiumStateVars = { "m": { 
                          "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                          "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
                    "h": { 
                            "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                            "beta": [1.00,0.00,1.00,35.00,-10.00]} 
                      }

    sodiumChannels = env.MembraneMechanism( 
                            MM_AlphaBetaChannel,
                            name="NaChl", ion="na",
                            equation="m*m*m*h",
                            conductance=unit("120:mS/cm2"),
                            reversalpotential=unit("50:mV"),
                            statevars=sodiumStateVars,
                            mechanism_id="HH_NA_CURRENT"
                            )
    kStateVars = { "n": { 
                          "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                          "beta": [0.125,0,0,65,80]},
                       }
    
    kChannels = env.MembraneMechanism( 
                            MM_AlphaBetaChannel,
                            name="KChl", ion="k",
                            equation="n*n*n*n",
                            conductance=unit("36:mS/cm2"),
                            reversalpotential=unit("-77:mV"),
                            statevars=kStateVars,
                            mechanism_id="HH_K_CURRENT"
                            )
    
    ApplyMechanismEverywhereUniform(myCell, leakChannels )
    ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
    ApplyMechanismEverywhereUniform(myCell, kChannels )
    
    


def apply_hh_chls_NEURON_builtin(env, myCell):

    hhChls = env.MembraneMechanism(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA" )
    ApplyMechanismEverywhereUniform(myCell, hhChls )
    





def simulate_chls_on_neuron(chl_applicator_functor):
    # Create the environment:
    env = NeuronSimulationEnvironment()
    
    # Create the simulation:
    mySim = env.Simulation()
    
    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    myCell = mySim.createCell(name="Cell1", morphology=m1)
    
    # Setup the HH-channels on the cell:
    chl_applicator_functor(env, myCell)
    
    # Setup passive channels:
    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
    
    
    
    
    # Get a location on the cell:
    somaLoc = myCell.getLocation("soma")
    
    # Create the stimulus and record the injected current:
    cc = mySim.createCurrentClamp( name="Stim1", amp=unit("100:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
    
    
    # Define what to record:
    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
    
    
    # Run the simulation
    results = mySim.Run()
    return results





resultsA = simulate_chls_on_neuron( apply_hh_chls_morphforge_format )
resultsB = simulate_chls_on_neuron( apply_hh_chls_NEURON_builtin )

# Display the results:
TagViewer([resultsA,resultsB], timeranges=[(95, 200)*pq.ms], show=True )


