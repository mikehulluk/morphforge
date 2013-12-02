





from morphforge.stdimports import *
from morphforgecontrib.stdimports import *



# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()


# Create a cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)
cell = sim.create_cell(name="Cell1", morphology=m1)


lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
k_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)


# Apply the channels uniformly over the cell
cell.apply_channel( lk_chl)
cell.apply_channel( na_chl)
cell.apply_channel( k_chl)
cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))

# Get a cell_location on the cell:


# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
sim.record(cc, what=StandardTags.Current)
# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)


sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
sim.record(na_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.ConductanceDensity)

sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
sim.record(na_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.CurrentDensity)


sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="m")
sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="h")
sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.StateVariable, state="n")


# Also:


# run the simulation
results = sim.run()


# Display the results, there is a lot of info for one graph, so lets split it up:
TagViewer([results], timerange=(50, 250)*units.ms, show=False)


TagViewer([results], timerange=(50, 250)*units.ms, show=False,
          plots = [
                       DefaultTagPlots.Voltage,
                       DefaultTagPlots.Current,
                       DefaultTagPlots.CurrentDensity,
                      ])


TagViewer([results], timerange=(100, 120)*units.ms, show=True,
          plots = [
                       DefaultTagPlots.Voltage,
                       DefaultTagPlots.ConductanceDensity,
                       DefaultTagPlots.StateVariable,
                      ])
