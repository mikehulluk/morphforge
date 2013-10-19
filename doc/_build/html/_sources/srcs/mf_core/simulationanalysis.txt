SimulationAnalysis Layer
========================


Traces
------
After simulations have been run, we might want to perform a variety
of analyses on the output. A common task is to analyse part of a recorded value, for
example for plotting or finding spike times from a membrane voltage. The analysis
might be more complex, for example calculating coupling coefficients between two
electrically coupled neurons using their deviations from resting potential in a partic-
ular time window following a step current injection to one of the neurons . We might
also want to compare a simulated membrane voltage trace against an experimentally
recorded one for example to find the difference as was done in Chapter 2.
These analogue signals are often represented as an array of times and an array of
values. In many cases, DEs can be solved efficiently using variable time-step integrat-
ors [Hindmarsh et al., 2005], which return values of the signal at irregularly spaced
times. This means that even simple operations such as adding two signals and may
require interpolation of values so that both signals use the same time values. Since
the time and data points for a single recording are coupled, it is useful to encapsulate
them together as a single object and define functions that operate on both together.
Morphforge builds a Trace class on top of the python-quantities and neurounit lib-
raries and encapsulates a time and signal-value array. The design of the Trace class
in morphforge supports both regular and irregularly spaced time-bases transparently.
The class has basic methods such as mean() and max() for simple analysis, and ad-
ditional methods can be added dynamically. Operators, such as +-/* are suitably
overloaded and return new Trace objects. The Trace objects transparently handle
units.
Listing D.10 illustrates how the input resistance of a neuron can be calculated. The
simulation code is omitted, but we assume that the voltage, V, is recorded from a
single neuron, which is given a step current injection of 30 pA from 100 ms to 200 ms.
We assume that the resting potential is reached after 50 ms and the steady state after
the current injection after 150 ms. This code will work regardless of whether variable
time steps are used in the simulation, and the resulting object will automatically
contain the correct units.

.. code-block:: python

    # <code to create, and run a simulation omitted>
    v = res.get_trace(’v’)
    result=(v.window(150, 200)*ms - v.window(50, 90)*ms).mean() / (-30*pA)



Trace Tags
-----------------

In a small network simulation, we may want to visualise the internal states of many
neurons and synapses — how do we effectively choose which values to plot or use
in other forms of analysis? Imagine we have two populations of neurons, P1 & P2,
synapses form stochastically between each pair of neurons in P1 and P2 with a prob-
ability of 0.3, and we want to plot the conductances of the synapses.
One option would be to store a handle from each call to record() for the conduct-
ance of each synapse. After simulation had run(), these handles could be used to
look up the corresponding Trace object in the SimulationResult object. Alternat-
ively, each call to record() could be passed an explicit name, as is done on line 29
in Listing 3.5, and later use this string to retrieve the relevant results. However both
mechanisms require adding complex code to the simulation script: if handles are
used, it is necessary to track which handle refers to which synapse recording and if
explicit string names are used, a suitable naming system will be required that can
cope with the stochasticity in the number of synapses. The situation quickly becomes
more complex, for example, to plot the conductance traces of all synapses which have
postsynaptic receptors on a particular neuron from a particular source population.
To solve this problem, morphforge introduces a system of tags in order to quickly
find Trace objects recorded in a simulation. Each Trace object contains a set of strings
called tags, which are used to attach contextual information about the Trace. The
tags can be specified by the user explicitly during the call to Simulation.record(),
(for example Listing D.9) and morphforge will also add certain tags automatically.
For example, ’Voltage’ or ’CurrentDensity’ will be automatically added if the
Trace object represents a voltage or current density recording and when recording
from a Synapse object, morphforge will automatically add the tags ’PRE:cell1’ and
’POST:cell2’ where cell1 and cell2 are the names of the presynaptic and postsyn-
aptic neurons respectively (more examples are given in the documentation).
A simple string-based language has been designed, for selecting specific sets of
Trace objects after a simulation has run. The language uses the keywords: ALL, ANY,
AND, OR and NOT. The terms ALL{A,B,..,C} and ANY{X,Y,...,Z} are matching pre-
dicates which take comma separated arguments. ALL{A,B,..,C} returns whether a
particular Trace contains all the tags specified (i. e. A, B, C) and ANY{X,Y,...,Z} re-
turns whether a Trace contains any of the tags specified (i. e. X, Y, Z). These match
predicates can be joined with the AND, OR and NOT operators as well as brackets to
allow more complex queries. For example, ALL{Voltage} will return all the voltages
recorded in the simulation and ALL{CONDUCTANCE,SYNAPTIC,PRE:cell1,POST:cell2}
AND ANY{NMDA,AMPA} could be used to retrieve all Trace objects representing conduct-
ances in AMPAR and NMDAR synapses from cell1 to cell2.
This system of tagging, and the use of conventions such as voltage traces always have
a ’Voltage’ tag allows looser coupling between different parts of the code and allows
more scripts to be more succinct.


Plotting with TagViewer
------------------------

The Trace object contains methods, time_pts_in() & data_pts_in() that return
numpy arrays of their time and data converted to specific units. These arrays can then
be used for analysis with other scientific Python libraries. Listing D.11 shows how a
Trace object can be plotted using the library matplotlib. Although this is one way of
plotting results, morphforge provides another class TagViewer which makes it much
less verbose to plot a selection of Trace objects from a simulation.

.. code-block:: python

    my_voltage_trace = result.get_trace(...)
    pylab.plot(my_voltage_trace.time_pts_in(’ms’), my_voltage_trace.data_pts_in(’mV’) )

    

The output of the TagViewer is a single figure, containing a series of axes with the
same time base. The details of each axis, such as the y-label, the appropriate display
range and unit are specified by PlotSpec objects. The PlotSpec object also takes a
tag-selection string, to define which Traces should be plot on that axis, and rather
than needing to explicitly specify which traces should be plot, the TagViewer object
directly queries the SimulationResults object. An example is given in Listing D.12,
in which two axes will be displayed, one in which contains all Traces containing the
tag ’Voltage’, and another which contains Traces with both Voltage and cell47 as tags.
TagViewer objects have a set of PlotSpecs that are used by default and will auto-
matically plot ’Voltage’, ’Current’, ’Conductance’ and other standard-tags. More
examples of the figures generated for different simulations by TagViewer are given in
Appendix E.


.. code-block:: python

    results = simulation.run()
    TagViewer(results,
        specs = [
            PlotSpec(’Voltage’,....)
            PlotSpec(’ALL{Voltage,cell47}’, ....)
    ])







Types
~~~~~~

Pluggable methods and operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




Simulation Summaries
--------------------
Models in computational neuroscience involve complex equations, many units and
have large numbers of parameters; a typical HH-type sodium channel has 7 equations
involving 12 parameters. Often modelling involves adjusting parameters. How do
we keep track of which parameters produce which results? Experimentalists use lab
notebooks as a way to record protocol setups but manually noting all the details
of a complex simulation is unfeasible. One approach is to use version control, for
example Sumatra [Davison, 2012]. An alternative approach is to generate summaries
of a simulation from the internal object-model to produce a human readable output
directly. The need for standard presentation formats for models has been recognised,
even if exact formats have not yet been defined (e. g. [Nordlie et al., 2009; Nordlie
and Plesser, 2010; Crook et al., 2012]).
Morphforge supports the production of html and pdf-document summaries from
Simulation objects directly using mredoc, (Modular Reduced Documentation) library.
This library is a high-level interface for producing documents containing images,
tables, code-snippets and equations for documenting mathematical models. After the
Simulation object has been populated, it can be summarised as shown in Listing D.13


.. code-block:: python 

    sim = env.Simulation()
    # Populate the simulation ...
    sim.create_cell(...)
    sim.create_synapse(...)
    # Summarise the object
    SummaryManager.summarise(simulation).to_pdf(’~/mysimulation.pdf’)

Simulations in morphforge can be populated with Synapse and Channel objects of
different types, for example NineML, NeuroML & neurounit. The summary architecture
allows these objects to create summaries of themselves. An example of summarising
a simulation and the resulting pdf document are given here.

.. todo::

    Copy example-pdf from Thesis to here.

    
:download:`An Example Pypi Project<docs/examplepypi.pdf>`
