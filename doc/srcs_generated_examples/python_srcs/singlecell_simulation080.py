







from morphforge.stdimports import *
from morphforgecontrib.stdimports import StandardModels


def sim(glk_multiplier, gna_multiplier, tag):
    
    env = NEURONEnvironment()
    sim = env.Simulation()

    # Create a cell:
    morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.3, soma_radius=9.0, axon_sections=20)
    cell = sim.create_cell(name="Cell1", morphology=morph)


    lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
    k_chl  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)

    # Apply the channels uniformly over the cell
    cell.apply_channel(lk_chl)
    cell.apply_channel(na_chl)
    cell.apply_channel(k_chl)

    # Over-ride the parameters in the axon:
    cell.apply_channel(channel=lk_chl, where="axon", parameter_multipliers={'gScale':glk_multiplier})
    cell.apply_channel(channel=na_chl, where="axon", parameter_multipliers={'gScale':gna_multiplier})

    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))


    for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=cell, distances=range(9, 3000, 100)):
        sim.record(cell, what=StandardTags.Voltage, cell_location=cell_location, user_tags=[tag])

    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)

    # run the simulation
    return sim.run()


# Display the results:
results_a = [
    sim(glk_multiplier=0.1, gna_multiplier=1.0, tag="SIM1"),
    sim(glk_multiplier=0.5, gna_multiplier=1.0, tag="SIM2"),
    sim(glk_multiplier=1.0, gna_multiplier=1.0, tag="SIM3"),
    sim(glk_multiplier=5.0, gna_multiplier=1.0, tag="SIM4"),
    sim(glk_multiplier=10.0, gna_multiplier=1.0, tag="SIM5"),
]

TagViewer(results_a, timerange=(97.5, 140)*units.ms, show=False,
          plots = [
                    TagPlot("ALL{Voltage,SIM1}", ylabel='gLeak: 0.1\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM2}", ylabel='gLeak: 0.5\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM3}", ylabel='gLeak: 1.0\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM4}", ylabel='gLeak: 5.0\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM5}", ylabel='gLeak: 10.0\nVoltage',yrange=(-80, 50)*units.mV, legend_labeller=None),
                       ])

results_b = [
    sim(gna_multiplier=0.1,  glk_multiplier=1.0, tag="SIM6"),
    sim(gna_multiplier=0.5,  glk_multiplier=1.0, tag="SIM7"),
    sim(gna_multiplier=0.75, glk_multiplier=1.0, tag="SIM8"),
    sim(gna_multiplier=1.0,  glk_multiplier=1.0, tag="SIM9"),
]

TagViewer(results_b, timerange=(97.5, 140)*units.ms, show=True,
          plots = [
                    TagPlot("ALL{Voltage,SIM6}", ylabel='gNa: 0.10\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM7}", ylabel='gNa: 0.50\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM8}", ylabel='gNa: 0.75\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                    TagPlot("ALL{Voltage,SIM9}", ylabel='gNa: 1.00\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                       ])

