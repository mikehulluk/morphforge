
======================
Morphforge Users Guide
======================



Introduction
============

morphforge is described in Mike Hull's Ph.D thesis (link) and this paper(link)

Modern simulators such as NEURON support a range of features; from modelling the internal diffusion of ions within a multicompartmental neuron to the calculation of extracellular potentials. It would require huge number of resources to implement a new interface that was the superset of these features. Rather than try to define a single monolithic system, the approach taken in morphforge is to provide a collection of classes and interfaces which form the core infrastructure, and then use a system of plugins which can be written to implement particular features. For example, morphforge is agnostic to how a synapse model is defined. The core of morphforge defines a minimal interface, and then plugins can be written, which allow a synapse specified in Python or MODL for example to be used with NEURON. This means morphforge naturally splits into two parts, morphforge-core, which contains the core infrastructure, and morphforge-contrib, which contains for example the plugins that define how a synapse model specified in a particular format is mapped to a particular simulator backend.

+------------------------+--------------------------------------------+--------------------------------------------------+
|                        | mf-core                                    | mf-contrib                                       |
+========================+============================================+==================================================+
| simulation-analysis    | * Plotting library                         |  * Trace analysis functions (e.g. spike counting)|
|                        | * summary generation infrastructure        |                                                  |
|                        |                                            |                                                  |
+------------------------+--------------------------------------------+--------------------------------------------------+
| simulation             | * classes for defining simulations, (e.g:  |  * mapping of synapse and                        |
|                        |   Cell, Synapse, GapJunction, Channel) and |    channel descriptions to                       |
|                        |   results (e.g. Trace, Event)              |    simulators, e.g.                              |
|                        | * NEURON backend support                   |    NEUROML -> NEURON                             |
+------------------------+--------------------------------------------+--------------------------------------------------+
| morphology             | * Classes for defining                     |  * import/export of                              |
|                        |   neuronal morphologies (e.g.              |    morphologies (e.g. .SWC)                      |
|                        |   Morphology, Segment,                     |  * visualisation                                 |
|                        |   Region, MorphLocation )                  |                                                  |
+------------------------+--------------------------------------------+--------------------------------------------------+
| core                   | * random number seeding & generation       |                                                  |
|                        | * file IO                                  |                                                  |
|                        |                                            |                                                  |
|                        |                                            |                                                  |
+------------------------+--------------------------------------------+--------------------------------------------------+


morphforge is split into four layers each defining a set of classes that work together as an object-model (Table. 1). The higher layers depend on the lower levels, but lower levels do not need the higher ones, for
example, Morphology objects are used by the simulation-layer, but can also be used without it, for example for anatomical reconstructions. The core-layer provides a single point of access to control random number
seeding, simulation settings and locations on the filesystem access as well as the plugin infrastructure and utility functions. The morphology-layer provides classes that represent neuronal morphologies as a
tree of cylinders and functions for their creation, import, export, rendering, traversal and manipulation. The simulation-layer defines a simulator independent object-model on top of the morphology objects
for defining multicompartmental neurons with complex channel distributions. Primitives for defining network connectivity and an interface for recording values during a simulation are also provided. It
provides a set of component-libraries to allow objects, such as morphologies, channels and synapses,to be defined once and reused with different parameters as well as an extensible high-level object-model
for representing analog signals with units. Finally, the simulationanalysis-layer provides functions for analysing the output of simulations such as spike detection, a visualisation system for easily viewing the
outputs of simulations and infrastructure for automatically generating summaries of simulations including the details of components such as channels and synapses.



morphforge-core
================

.. toctree::
    :maxdepth: 2
    
    /srcs/mf_core/morphology.rst
    /srcs/mf_core/simulation.rst
    /srcs/mf_core/simulation_neuron.rst
    /srcs/mf_core/simulationanalysis.rst
    /srcs/mf_core/misc.rst



morphforge-contrib
==================


.. toctree::
    :maxdepth: 3

    /srcs/mf_contrib/morphology.rst
    /srcs/mf_contrib/simulation.rst
    /srcs/mf_contrib/simulation_analysis.rst

Reference
=========

.. toctree::


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
