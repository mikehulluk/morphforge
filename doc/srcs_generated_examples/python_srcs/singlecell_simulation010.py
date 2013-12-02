






from morphforge.stdimports import *
from morphforgecontrib.stdimports import StdChlLeak


# Create the morphology for the cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)

# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()


# Create a cell:
cell = sim.create_cell(name="Cell1", morphology=m1)


# Apply the mechanisms to the cells
lk_chl = env.Channel(StdChlLeak,
                         name="LkChl",
                         conductance=qty("0.25:mS/cm2"),
                         reversalpotential=qty("-51:mV"),
                       )

cell.apply_channel( lk_chl)
cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))



# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=qty("200:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)


# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
sim.recordall(lk_chl, cell_location=cell.soma)


# run the simulation
results = sim.run()

# Create an output .pdf
SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')


# Display the results:
TagViewer([results], figtitle="The response of a neuron to step current injection", timerange=(95, 200)*units.ms, show=True)



