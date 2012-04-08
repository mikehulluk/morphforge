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



"""[*] Visualising action potential propogation
In this simulation, we create a cell with a long axon. We put HH-channels over its surface
and give it a short current injection into the soma. We look at the voltage at various points
along the axon, and see it propogate. 

"""


from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel


# Create the environment:
env = NeuronSimulationEnvironment()

# Create the simulation:
mySim = env.Simulation()

# Create a cell:
morph = MorphologyBuilder.getSomaAxonMorph(axonLength=3000.0, axonRad=0.15, somaRad=9.0, axonSections=20)
myCell = mySim.createCell(name="Cell1", morphology=morph)


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


# Apply the channels uniformly over the cell
ApplyMechanismEverywhereUniform(myCell, leakChannels )
ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
ApplyMechanismEverywhereUniform(myCell, kChannels )
ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )

# Get a location on the cell:
somaLoc = myCell.getLocation("soma")

# Create the stimulus and record the injected current:
cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), celllocation=somaLoc)
mySim.record( cc, what=StdRec.Current)



# To record along the axon, we create a set of 'CellLocations', at the distances 
# specified (start,stop,  
for cell_location in CellLocator.getLocationsAtDistancesAwayFromDummy(cell=myCell, distances=range(9, 3000, 100) ):

    print " -- ",cell_location.section
    print " -- ",cell_location.sectionpos
    print " -- ",cell_location.get_3d_position()
    
    # Create a path along the morphology from the centre of the 
    # Soma
    path = MorphPath( somaLoc, cell_location)
    print "Distance to Soma Centre:", path.get_length()
    
    mySim.record( myCell, what=StdRec.MembraneVoltage, location=cell_location, description="Distance Recording at %0.0f (um)"% path.get_length() )
    

# Define what to record:
mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 

# Run the simulation
results = mySim.Run()

# Display the results:
TagViewer([results], timeranges=[(97.5, 140)*pq.ms] )
