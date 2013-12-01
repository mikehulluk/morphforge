






from morphforge.stdimports import *
from morphforgecontrib.stdimports import StdChlLeak, StdChlAlphaBeta


@cached_functor
def get_Na_Channels(env):
    na_state_vars = {"m":
                    {"alpha": [13.01,0,4,-1.01,-12.56], "beta": [5.73,0,1,9.01,9.69] },
                   "h":
                    {"alpha": [0.06,0,0,30.88,26], "beta": [3.06,0,1,-7.09,-10.21]}
                   }

    return  env.Channel(
                            StdChlAlphaBeta,
                            name="NaChl", ion="na",
                            equation="m*m*m*h",
                            conductance=qty("210:nS") / qty("400:um2"),
                            reversalpotential=qty("50.0:mV"),
                            statevars=na_state_vars,
                           )

@cached_functor
def get_Ks_Channels(env):
    kf_state_vars = {"ks": {"alpha": [0.2,0,1,-6.96,-7.74 ], "beta": [0.05,0,2,-18.07,6.1 ] } }

    return  env.Channel(
                            StdChlAlphaBeta,
                            name="KsChl", ion="ks",
                            equation="ks*ks*ks*ks",
                            conductance=qty("3:nS") / qty("400:um2"),
                            reversalpotential=qty("-80.0:mV"),
                            statevars=kf_state_vars,
                           )

@cached_functor
def get_Kf_Channels(env):
    kf_state_vars = {"kf": {"alpha": [ 3.1,0,1,-31.5,-9.3], "beta": [0.44,0,1,4.98,16.19 ] } }

    return  env.Channel(
                            StdChlAlphaBeta,
                            name="KfChl", ion="kf",
                            equation="kf*kf*kf*kf",
                            conductance=qty("0.5:nS") / qty("400:um2") ,
                            reversalpotential=qty("-80.0:mV"),
                            statevars=kf_state_vars,
                           )

@cached_functor
def get_Lk_Channels(env):
    lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=qty("3.6765:nS") / qty("400:um2"),
                         reversalpotential=qty("-51:mV"),
                       )
    return lk_chl




def simulate(current_inj_level):
    # Create the environment:
    env = NEURONEnvironment()

    # Create the simulation:
    sim = env.Simulation(name="AA")


    # Create a cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    morph = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(name="Cell1", morphology=morph)

    lk_chl = get_Lk_Channels(env)
    na_chl = get_Na_Channels(env)
    potFastChannels = get_Kf_Channels(env)
    potSlowChannels = get_Ks_Channels(env)

    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( potFastChannels)
    cell.apply_channel( potSlowChannels)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('2.0:uF/cm2'))



    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(amp=current_inj_level, dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)

    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, cell_location = cell.soma)

    # run the simulation
    results = sim.run()

    return results


# Display the results:
#results = [simulate(current_inj_level='%d:pA' % i) for i in [50,100,150,200, 250, 300]  ]
results = [simulate(current_inj_level='%d:pA' % i) for i in [50]  ]


# Create an output .pdf of the first simulation:
SimulationMRedoc.build( results[0] ).to_pdf(__file__ + '.pdf')

TagViewer(results, timerange=(95, 200)*units.ms, show=True)



