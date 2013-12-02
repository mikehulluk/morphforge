





from morphforge.stdimports import *
from morphforgecontrib.stdimports import *



def run_sim(axon_compartment_length):
    
    env = NEURONEnvironment()
    sim = env.Simulation()

    # Create a cell, consisting of a soma and long axon:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma', 'sections': [ {'length':4000,'diam':0.3, 'id':'axon'} ] } }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(
                name="Cell1", 
                morphology=m1, 
                segmenter=CellSegmenter_MaxLengthByID(section_id_segment_maxsizes={'soma':20,'axon':axon_compartment_length} ) 
                )

    lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
    k_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)

    # Apply the channels uniformly over the cell
    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))

    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current, user_tags=['AxonCompLength%d'%axon_compartment_length])

    # Define a series of points at 50um intervals along the axon to record voltage at:
    pts_along_cell = CellLocator.get_locations_at_distances_away_from_dummy(cell=cell, distances= [0] + list(range(20,4000, 10) ) )
    x0 = CellLocator.get_location_at_distance_away_from_dummy(cell=cell, distance=20 ).morphlocation

    for pt in pts_along_cell:
        dist = "Distance%04d"%MorphPath(x0, pt.morphlocation).get_length()
        sim.record(cell, what=StandardTags.Voltage, description=dist, user_tags=['AxonCompLength%d'%axon_compartment_length], cell_location = pt)

    # run the simulation
    results = sim.run()
    return results




axon_compartment_lengths = [20,50,100,200,500]
results = [ run_sim(axon_compartment_length=ax_comp_len) for ax_comp_len in axon_compartment_lengths]

TagViewer(results, 
          timerange=(98, 125)*units.ms,
          plots = 
                [ TagPlot("ALL{Voltage,AxonCompLength%d}"%ax_comp_len, ylabel='Axon comp \n Length:%dum\n (Voltage)'%ax_comp_len, yrange=(-80*units.mV, 50*units.mV), yunit=units.mV,  legend_labeller=None, yticklabel_quantisation=Decimal('1')) for ax_comp_len in axon_compartment_lengths] +
                [ TagPlot("ALL{Current,AxonCompLength20}", ylabel='Current', yunit=units.picoamp, yticklabel_quantisation=Decimal('1') ) ]
                  )



