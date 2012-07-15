
17. Applying different channel densities over a cell
====================================================


Applying different channel densities over a cell.
We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface.
We look at the effect of changing the density of leak and sodium channels in just the axon
of the neuron (not the soma)

This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and
then tell the TagViewer to plot everything with a tag 'SIMY'

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.data_library.stdmodels import StandardModels
	
	
	def sim( glk_multiplier, gna_multiplier, tag):
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	
	    # Create the simulation:
	    mySim = env.Simulation()
	
	    # Create a cell:
	    morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.3, soma_radius=9.0, axon_sections=20)
	    myCell = mySim.create_cell(name="Cell1", morphology=morph)
	
	
	    lkChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
	    naChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
	    kChannels  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)
	
	    # Apply the channels uniformly over the cell
	    apply_mechanism_everywhere_uniform(myCell, lkChannels )
	    apply_mechanism_everywhere_uniform(myCell, naChannels )
	    apply_mechanism_everywhere_uniform(myCell, kChannels )
	
	    # Over-ride the parameters in the axon:
	    apply_mechanism_region_uniform(cell=myCell, mechanism=lkChannels, region=morph.get_region("axon"), parameter_multipliers={'gScale':glk_multiplier})
	    apply_mechanism_region_uniform(cell=myCell, mechanism=naChannels, region=morph.get_region("axon"), parameter_multipliers={'gScale':gna_multiplier})
	
	    apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
	    for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=myCell, distances=range(9, 3000, 100) ):
	        mySim.record( myCell, what=StandardTags.Voltage, cell_location=cell_location, user_tags=[tag])
	
	    # Create the stimulus and record the injected current:
	    cc = mySim.create_currentclamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), cell_location=myCell.get_location("soma"))
	    mySim.record( cc, what=StandardTags.Current)
	
	    # run the simulation
	    return mySim.run()
	
	
	# Display the results:
	results_a = [
	    sim( glk_multiplier=0.1, gna_multiplier=1.0, tag="SIM1"),
	    sim( glk_multiplier=0.5, gna_multiplier=1.0, tag="SIM2"),
	    sim( glk_multiplier=1.0, gna_multiplier=1.0, tag="SIM3"),
	    sim( glk_multiplier=5.0, gna_multiplier=1.0, tag="SIM4"),
	    sim( glk_multiplier=10.0, gna_multiplier=1.0, tag="SIM5"),
	]
	
	TagViewer(results_a, timeranges=[(97.5, 140)*pq.ms], show=False,
	          plotspecs = [
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM1}", ylabel='gLeak: 0.1\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM2}", ylabel='gLeak: 0.5\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM3}", ylabel='gLeak: 1.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM4}", ylabel='gLeak: 5.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM5}", ylabel='gLeak: 10.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                        ] )
	
	results_b = [
	    sim( gna_multiplier=0.1,  glk_multiplier=1.0, tag="SIM6"),
	    sim( gna_multiplier=0.5,  glk_multiplier=1.0, tag="SIM7"),
	    sim( gna_multiplier=0.75,  glk_multiplier=1.0, tag="SIM8"),
	    sim( gna_multiplier=1.0,  glk_multiplier=1.0, tag="SIM9"),
	]
	
	TagViewer(results_b, timeranges=[(97.5, 140)*pq.ms],show=True,
	          plotspecs = [
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM6}", ylabel='gNa: 0.10\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM7}", ylabel='gNa: 0.50\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM8}", ylabel='gNa: 0.75\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM9}", ylabel='gNa: 1.00\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                        ] )
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out2.png>`






Output
~~~~~~

.. code-block:: bash

    	2012-07-15 16:21:51,742 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:51,742 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x97cb40c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x9803fcc>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x9805f0c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x97d1d0c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x970b84c>
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa33166c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa417c2c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x97cc28c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x97d72ac>
	Saving File _output/figures/singlecell_simulation080/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation080/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation080/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation080/svg/fig000_Autosave_figure_1.svg
	Saving File _output/figures/singlecell_simulation080/eps/fig001_Autosave_figure_2.eps
	Saving File _output/figures/singlecell_simulation080/pdf/fig001_Autosave_figure_2.pdf
	Saving File _output/figures/singlecell_simulation080/png/fig001_Autosave_figure_2.png
	Saving File _output/figures/singlecell_simulation080/svg/fig001_Autosave_figure_2.svg
	




