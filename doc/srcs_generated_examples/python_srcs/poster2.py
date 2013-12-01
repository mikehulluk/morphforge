








import matplotlib as mpl
mpl.rcParams['font.size'] = 14


from morphforge.stdimports import *
from morphforgecontrib.stdimports import *

# Create a cell:
def build_cell(name, sim):

    my_morph = MorphologyBuilder.get_soma_axon_morph(axon_length=1500.0, axon_radius=0.3, soma_radius=10.0)
    my_cell = sim.create_cell(name=name, morphology=my_morph)

    na_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=sim.environment)
    k_chls  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K",  env=sim.environment)
    lk_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=sim.environment)

    my_cell.apply_channel(lk_chls)
    my_cell.apply_channel(k_chls)
    my_cell.apply_channel(na_chls)
    my_cell.apply_channel(na_chls, where="axon", parameter_multipliers={'gScale':1.0})
    return my_cell


# Create a simulation:
env = NEURONEnvironment()
sim = env.Simulation()

# Two cells:
cell1 = build_cell(name="cell1", sim=sim)
cell2 = build_cell(name="cell2", sim=sim)
cell3 = build_cell(name="cell3", sim=sim)


# Connect with a synapse:
simple_ampa_syn = """
define_component syn_simple {

    g' = - g/g_tau
    i = gmax * (v-erev) * g

    gmax = 300pS * scale
    erev = 0mV

    g_tau = 10ms
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> PARAMETER scale:()
    on on_event(){
        g = g + 1.0
    }
}
"""


post_syn_tmpl = env.PostSynapticMechTemplate(
        NeuroUnitEqnsetPostSynaptic,
        eqnset = simple_ampa_syn,
        default_parameters = { 'scale':1.0}
        )

syn1 = sim.create_synapse(
        trigger =  env.SynapticTrigger(
                                    SynapticTriggerByVoltageThreshold,
                                        cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 300),
                                        voltage_threshold = qty("0:mV"),  delay=qty("0:ms"), 
                                   ),
        postsynaptic_mech = post_syn_tmpl.instantiate(cell_location = cell2.soma,), 
       )

syn1 = sim.create_synapse(
        trigger =  env.SynapticTrigger(
                                    SynapticTriggerByVoltageThreshold,
                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 700),
                                    voltage_threshold = qty("0:mV"),  delay = qty("0:ms"),
                                   ),
        postsynaptic_mech = post_syn_tmpl.instantiate(cell_location = cell3.soma, parameter_overrides={'scale':2.0} )  
       )

# Record Voltages from axons:
for loc in CellLocator.get_locations_at_distances_away_from_dummy(cell1, range(0, 1000, 50)):
    sim.record( what=StandardTags.Voltage, cell_location = loc, user_tags=['cell1'])
sim.record(what=StandardTags.Voltage, cell_location = cell2.get_location("soma"), user_tags=['cell2'])
sim.record(what=StandardTags.Voltage, cell_location = cell3.get_location("soma"), user_tags=['cell3'])

# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="CC1", amp=qty("200:pA"), dur=qty("1:ms"), delay=qty("100:ms"), cell_location=cell1.get_location("soma"))
sim.record(cc, what=StandardTags.Current)

results = sim.run()
TagViewer(results, timerange=(98, 120)*units.ms,
          fig_kwargs = {'figsize':(12, 10)},
          show=True,
          plots = [
              TagPlot('Current', yunit=units.picoamp),
              TagPlot('Voltage,cell1', yrange=(-80*units.mV, 50*units.mV), yunit=units.mV),
              TagPlot('Voltage AND ANY{cell2,cell3}', yrange=(-70*units.mV, -55*units.mV), yunit=units.millivolt),
             ],
           )


