







from morphforge.stdimports import *
from morphforgecontrib.stdimports import StdChlLeak,StdChlAlphaBeta

# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()

# Create a cell:
morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.15, soma_radius=9.0, axon_sections=20)
cell = sim.create_cell(name="Cell1", morphology=morph)


lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=qty("0.3:mS/cm2"),
                         reversalpotential=qty("-54.3:mV"),
                       )

na_state_vars = { "m": {
                      "alpha":[-4.00, -0.10, -1.00, 40.00, -10.00],
                      "beta": [4.00, 0.00, 0.00, 65.00, 18.00]},
                    "h": {
                        "alpha":[0.07, 0.00, 0.00, 65.00, 20.00] ,
                        "beta": [1.00, 0.00, 1.00, 35.00, -10.00]}
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
                      "alpha":[-0.55, -0.01, -1.0, 55.0, -10.0],
                      "beta": [0.125, 0, 0, 65, 80]},
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
cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
sim.record(cc, what=StandardTags.Current)



# To record along the axon, we create a set of 'CellLocations', at the distances
# specified (start, stop,
for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=cell, distances=range(9, 3000, 100)):

    print " -- ", cell_location.section
    print " -- ", cell_location.sectionpos
    print " -- ", cell_location.get_3d_position()

    # Create a path along the morphology from the centre of the
    # Soma
    path = MorphPath(cell.soma, cell_location)
    print "Distance to Soma Centre:", path.get_length()

    sim.record(cell, what=StandardTags.Voltage, cell_location=cell_location, description="Distance Recording at %0.0f (um)"% path.get_length())


# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)

# run the simulation
results = sim.run()

# Display the results:
TagViewer([results], timerange=(97.5, 140)*units.ms)
