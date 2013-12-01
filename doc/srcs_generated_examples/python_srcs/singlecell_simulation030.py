








from morphforge.stdimports import *
from morphforgecontrib.stdimports import StdChlLeak, StdChlAlphaBeta

# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()


# Create a cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)
cell = sim.create_cell(name="Cell1", morphology=m1)


lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=qty("0.3:mS/cm2"),
                         reversalpotential=qty("-54.3:mV"),
                       )

na_state_vars = { "m": {
                      "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                      "beta": [4.00, 0.00, 0.00,65.00, 18.00]},
                    "h": {
                        "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                        "beta": [1.00,0.00,1.00,35.00,-10.00]}
                  }

na_chl = env.Channel(
                        StdChlAlphaBeta,
                        name="NaChl", ion="na",
                        equation="m*m*m*h",
                        conductance=qty("120:mS/cm2"),
                        reversalpotential=qty("50:mV"),
                        statevars=na_state_vars,
                       )
k_state_vars = { "n": {
                      "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                      "beta": [0.125,0,0,65,80]},
                   }

k_chl = env.Channel(
                        StdChlAlphaBeta,
                        name="KChl", ion="k",
                        equation="n*n*n*n",
                        conductance=qty("36:mS/cm2"),
                        reversalpotential=qty("-77:mV"),
                        statevars=k_state_vars,
                        
                       )


# Apply the channels uniformly over the cell
cell.apply_channel( lk_chl)
cell.apply_channel( na_chl)
cell.apply_channel( k_chl)
cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))


# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
sim.record(cc, what=StandardTags.Current)
# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)

# run the simulation
results = sim.run()


# Create an output .pdf
SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')

# Display the results:
TagViewer([results], timerange=(50, 250)*units.ms, show=True)


