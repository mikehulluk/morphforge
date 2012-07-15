import matplotlib as mpl
mpl.rcParams['font.size'] = 14



from morphforge.stdimports import *
from morphforgecontrib.stdimports import *

# Create a cell:
def build_cell(name,sim):

    my_morph = MorphologyBuilder.get_soma_axon_morph(axon_length=1500.0, axon_radius=0.3, soma_radius=10.0, )
    my_cell = sim.create_cell(name=name, morphology=my_morph)

    na_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=sim.environment)
    k_chls  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K",  env=sim.environment)
    lk_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=sim.environment)

    apply_mechanism_everywhere_uniform(my_cell, lk_chls )
    apply_mechanism_everywhere_uniform(my_cell, k_chls )
    apply_mechanism_everywhere_uniform(my_cell, na_chls )
    apply_mechanism_region_uniform( my_cell,
                                    na_chls,
                                    region = my_cell.get_region("axon"),
                                    parameter_multipliers={'gScale':1.0} )
    return my_cell


# Create a simulation:
env = NeuronSimulationEnvironment()
sim = env.Simulation()

# Two cells:
cell1 = build_cell(name="cell1",sim=sim)
cell2 = build_cell(name="cell2",sim=sim)
cell3 = build_cell(name="cell3",sim=sim)


# Connect with a synapse:
simple_ampa_syn = """
EQNSET syn_simple {

    g' = - g/g_tau
    i = gmax * (v-erev) * g

    gmax = 300pS * scale
    erev = 0mV

    g_tau = 10ms
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> PARAMETER scale:()
    ==>> on_event() {
        g = g + 1.0
    }
}
"""


syn1 = sim.create_synapse(
        presynaptic_mech =  env.PreSynapticMechanism(
                                    PreSynapticMech_VoltageThreshold,
                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 300),
                                    voltage_threshold = U("0:mV"),  delay = U("0:ms"),     weight = U("1:nS"),
                                    ),
        postsynaptic_mech = env.PostSynapticMechanism(
                                    NeuroUnitEqnsetPostSynaptic,
                                    eqnset = neurounits.NeuroUnitParser.EqnSet(simple_ampa_syn),
                                    default_parameters= {'scale':1.0*pq.dimensionless},
                                    cell_location = cell2.get_location("soma")
                                    )
        )

syn1 = sim.create_synapse(
        presynaptic_mech =  env.PreSynapticMechanism(
                                    PreSynapticMech_VoltageThreshold,
                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 700),
                                    voltage_threshold = U("0:mV"),  delay = U("0:ms"), weight = U("1:nS"),
                                    ),
        postsynaptic_mech = env.PostSynapticMechanism(
                                    NeuroUnitEqnsetPostSynaptic,
                                    eqnset = neurounits.NeuroUnitParser.EqnSet(simple_ampa_syn),
                                    default_parameters= {'scale':2.0*pq.dimensionless},
                                    cell_location = cell3.get_location("soma")
                                    )
        )

# Record Voltages from axons:
for loc in CellLocator.get_locations_at_distances_away_from_dummy( cell1, range(0,1000,50) ):
    sim.record(  what=StandardTags.Voltage, cell_location = loc, user_tags=['cell1'] )
sim.record( what=StandardTags.Voltage, cell_location = cell2.get_location("soma"), user_tags=['cell2'] )
sim.record( what=StandardTags.Voltage, cell_location = cell3.get_location("soma"), user_tags=['cell3'] )

# Create the stimulus and record the injected current:
cc = sim.create_currentclamp( name="CC1", amp=U("200:pA"), dur=U("1:ms"), delay=U("100:ms"), cell_location=cell1.get_location("soma"))
sim.record(cc, what=StandardTags.Current)

results = sim.run()
TagViewer(results, timeranges=[(98, 120)*pq.ms], 
          fig_kwargs = {'figsize':(12,10)},
          show=True,
          plotspecs = [
              PlotSpec_DefaultNew('Current', yunit=pq.picoamp),
              PlotSpec_DefaultNew('Voltage,cell1', yrange=(-80*mV,50*mV), yunit=pq.mV ),
              PlotSpec_DefaultNew('Voltage AND ANY{cell2,cell3}', yrange=(-70*mV,-55*mV), yunit=pq.millivolt),
              ],
            )


