"""Demonstrate using NEURON mod files directly in a simulation
We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.

"""


from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel


def build_simulation(modfilename):
    # Create the morphology for the cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    
    
    # Create the environment:
    env = NeuronSimulationEnvironment()
    
    # Create the simulation:
    mySim = env.Simulation()
    myCell = mySim.createCell(morphology=m1)
    somaLoc = myCell.getLocation("soma")
    
    modChls = env.MembraneMechanism( SimulatorSpecificChannel, 
                                     modfilename =  modfilename, 
                                     mechanism_id='ID1')
                                          
    # Apply the mechanisms to the cells
    ApplyMechanismEverywhereUniform(myCell, modChls )
    
    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc, description='Membrane Voltage')
    mySim.createCurrentClamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
    
    results = mySim.Run()
    return results



mod3aFilename = Join(LocMgr.getTestModsPath(), "exampleChannels3a.mod")
results3a = build_simulation( mod3aFilename )

mod3bFilename = Join(LocMgr.getTestModsPath(), "exampleChannels3b.mod")
results3b = build_simulation( mod3bFilename )

TagViewer([results3a,results3b], timeranges=[(95, 200)*pq.ms] )

try:
    import os
    print 'Differences between the two mod files:'
    os.system("diff %s %s"%(mod3aFilename,mod3bFilename) )
except:
    print "<Can't run 'diff', so can't show differences!>"




















