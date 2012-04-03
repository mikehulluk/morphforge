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
"""Single compartment with leak channels response to current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a current clamp"""
 
 

from morphforge.stdimports import *
#from morphforgecontrib.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel


# Create the morphology for the cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)

# Create the environment:
env = NeuronSimulationEnvironment()

# Create the simulation:
mySim = env.Simulation(name="TestSim1")


# Create a cell:
myCell = mySim.createCell(name="Cell1", morphology=m1)


# Apply the mechanisms to the cells
leakChannels = env.MembraneMechanism( MM_LeakChannel, 
                         name="LkChl", 
                         conductance=unit("0.25:mS/cm2"), 
                         reversalpotential=unit("-51:mV"),
                         mechanism_id = 'HULL12_DIN_LK_ID'
                        )
    
shortcuts.ApplyMechanismEverywhereUniform(myCell, leakChannels )
shortcuts.ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )


# Get a location on the cell:
somaLoc = myCell.getLocation("soma")

# Create the simulous:
mySim.createCurrentClamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)


# Define what to record:
mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) #, description='Membrane Voltage')
mySim.recordall( leakChannels, where=somaLoc)



# Run the simulation
results = mySim.Run()

#SimulationSummariser(simulationresult=results, filename="/home/michael/Desktop/outBlha.pdf", make_graphs=True)
# Display the results:
TagViewer([results], timeranges=[(95, 200)*pq.ms], show=False )
import pylab
pylab.show()


