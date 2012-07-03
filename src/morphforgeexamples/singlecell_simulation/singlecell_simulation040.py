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



"""Investigating the rheobase of a neuron with a parameter sweep

WARNING: The automatic naming and linkage between grpah colors is currently under a refactor;
what is done in this script is not representing the best possible solution, or even something that
will reliably work in the future!

The aim of this script is just to show that it is possible to run multiple simulations from a single script!




"""


from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel



def get_Na_Channels(env):
    naStateVars = {"m":
                    {"alpha": [ 13.01,0,4,-1.01,-12.56 ], "beta": [5.73,0,1,9.01,9.69 ] },
                   "h":
                    {"alpha": [ 0.06,0,0,30.88,26 ], "beta": [3.06,0,1,-7.09,-10.21 ]}
                   }

    return  env.MembraneMechanism(
                            MM_AlphaBetaChannel,
                            name="NaChl", ion="na",
                            equation="m*m*m*h",
                            conductance=unit("210:nS") / unit("400:um2"),
                            reversalpotential=unit("50.0:mV"),
                            statevars=naStateVars,
                            mechanism_id = 'Na_ID'
                            )

def get_Ks_Channels(env):
    kfStateVars = {"ks": {"alpha": [ 0.2,0,1,-6.96,-7.74  ], "beta": [0.05,0,2,-18.07,6.1  ] } }

    return  env.MembraneMechanism(
                            MM_AlphaBetaChannel,
                            name="KsChl", ion="ks",
                            equation="ks*ks*ks*ks",
                            conductance=unit("3:nS") / unit("400:um2"),
                            reversalpotential=unit("-80.0:mV"),
                            statevars=kfStateVars,
                            mechanism_id = 'IN_Ks_ID'
                            )

def get_Kf_Channels(env):
    kfStateVars = {"kf": {"alpha": [  3.1,0,1,-31.5,-9.3 ], "beta": [0.44,0,1,4.98,16.19  ] } }

    return  env.MembraneMechanism(
                            MM_AlphaBetaChannel,
                            name="KfChl", ion="kf",
                            equation="kf*kf*kf*kf",
                            conductance=unit("0.5:nS") / unit("400:um2") ,
                            reversalpotential=unit("-80.0:mV"),
                            statevars=kfStateVars,
                            mechanism_id = 'N_Kf_ID'
                            )

def get_Lk_Channels(env):
    leakChannels = env.MembraneMechanism(
                         MM_LeakChannel,
                         name="LkChl",
                         conductance=unit("3.6765:nS") / unit("400:um2"),
                         reversalpotential=unit("-51:mV"),
                         mechanism_id = 'Lk_ID'
                        )
    return leakChannels




def simulate(current_inj_level):
    # Create the environment:
    env = NeuronSimulationEnvironment()

    # Create the simulation:
    mySim = env.Simulation(name="AA")


    # Create a cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    morph = MorphologyTree.fromDictionary(morphDict1)
    myCell = mySim.create_cell(name="Cell1", morphology=morph)

    leakChannels = get_Lk_Channels(env)
    sodiumChannels = get_Na_Channels(env)
    potFastChannels = get_Kf_Channels(env)
    potSlowChannels = get_Ks_Channels(env)

    apply_mechanism_everywhere_uniform(myCell, leakChannels )
    apply_mechanism_everywhere_uniform(myCell, sodiumChannels )
    apply_mechanism_everywhere_uniform(myCell, potFastChannels )
    apply_mechanism_everywhere_uniform(myCell, potSlowChannels )
    apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('2.0:uF/cm2') )


    # Get a cell_location on the cell:
    somaLoc = myCell.get_location("soma")

    # Create the stimulus and record the injected current:
    cc = mySim.create_currentclamp( amp=current_inj_level, dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
    mySim.record(cc, what=StdRec.Current)

    # Define what to record:
    mySim.record( myCell, what=StdRec.MembraneVoltage, cell_location = somaLoc )

    # run the simulation
    results = mySim.run()

    return results


# Display the results:
results = [ simulate(current_inj_level='%d:pA'%i) for i in [50,100,150,200, 250, 300]   ]
TagViewer(results, timeranges=[(95, 200)*pq.ms], show=True )

