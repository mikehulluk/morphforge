






from morphforge.stdimports import *
from morphforgecontrib.simulation.channels.exisitingmodfile.core import SimulatorSpecificChannel


def build_simulation(modfilename):
    # Create the morphology for the cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)


    # Create the environment:
    env = NEURONEnvironment()

    # Create the simulation:
    sim = env.Simulation()
    cell = sim.create_cell(morphology=m1)


    modChls = env.Channel(SimulatorSpecificChannel, modfilename=modfilename)

    # Apply the mechanisms to the cells
    cell.apply_channel( modChls)

    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma, description='Membrane Voltage')
    sim.create_currentclamp(name="Stim1", amp=qty("200:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)

    results = sim.run()
    return results



mod3aFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3a.mod")
results3a = build_simulation(mod3aFilename)

mod3bFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3b.mod")
results3b = build_simulation(mod3bFilename)

TagViewer([results3a, results3b], timerange=(95, 200)*units.ms)

try:
    import os
    print 'Differences between the two mod files:'
    os.system("diff %s %s"%(mod3aFilename, mod3bFilename))
except:
    print "<Can't run 'diff', so can't show differences!>"





















