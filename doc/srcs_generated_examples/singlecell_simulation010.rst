
7. The response of a single compartment neuron with leak channels to step current injection
===========================================================================================


The response of a single compartment neuron with leak channels to step current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a step current clamp of 200pA for 100ms starting at t=100ms.
We also create a summary pdf of the simulation.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
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
    #SimulationSummariser(simulationresult=results, filename="Simulation010Output.pdf", make_graphs=True)
    
    # Display the results:
    TagViewer([results], figtitle="The response of a neuron to step current injection", timerange=(95, 200)*units.ms, show=True)
    
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation010_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:39:59,418 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:39:59,418 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:00,945 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:00,945 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/76/76c59b27246b597ce308e166527c4818.bundle (10k) : 0.799 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(2.5) * s**3*A**2/(kg*m**4)}
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_7898982be05f1f2a05fa869a234295a3.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_5392
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_7898982be05f1f2a05fa869a234295a3.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_7898982be05f1f2a05fa869a234295a3.lo tmp_7898982be05f1f2a05fa869a234295a3.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_7898982be05f1f2a05fa869a234295a3.la  -rpath /opt/nrn//x86_64/libs  tmp_7898982be05f1f2a05fa869a234295a3.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_7898982be05f1f2a05fa869a234295a3.c  -fPIC -DPIC -o .libs/tmp_7898982be05f1f2a05fa869a234295a3.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_7898982be05f1f2a05fa869a234295a3.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_7898982be05f1f2a05fa869a234295a3.so.0 -o .libs/tmp_7898982be05f1f2a05fa869a234295a3.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_7898982be05f1f2a05fa869a234295a3.so.0" && ln -s "tmp_7898982be05f1f2a05fa869a234295a3.so.0.0.0" "tmp_7898982be05f1f2a05fa869a234295a3.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_7898982be05f1f2a05fa869a234295a3.so" && ln -s "tmp_7898982be05f1f2a05fa869a234295a3.so.0.0.0" "tmp_7898982be05f1f2a05fa869a234295a3.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_7898982be05f1f2a05fa869a234295a3.la" && ln -s "../tmp_7898982be05f1f2a05fa869a234295a3.la" "tmp_7898982be05f1f2a05fa869a234295a3.la" )
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_c5c08b6d3f6b33550fdf990390eaee24.so
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (3 records) 0.0062689781189
    Running simulation : 0.529 seconds
    Post-processing : 0.002 seconds
    Entire load-run-save time : 1.330 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/singlecell_simulation010/{png,svg}/fig000_Autosave_figure_1.{png,svg}




