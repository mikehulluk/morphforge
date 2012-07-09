<<<<<<< HEAD
Overview
=========

Sub-Packages and Layers
~~~~~~~~~~~~~~~~~~~~~~~~

Morphforge is a large package; it has been split into
2 main packages:

 * `morphforge` contains the core object API for the object models.
 * `morphforgecontrib` contains 'data' code, for example, the definitions of 
   channel and synapse types.

Morphforge has 4 main layers:
  * `core` 
  * `morphology`
  * `simulation`
  * `simulation analysis`

which build on top of each other. You can use the `morphology` layer to work with 
morphologies with no knowledge of the `simulation` layer. However, the `simulation`
layer references both the `core` and `morphology` layers.  Both `morphforge` and `morphforgecontrib` have similar directories, reflecting
these layers. 

morphforge also contains the following directories:

 * `constants` - Defines some common constants
 * `componentlibraries` - Infrastructure to make component tracking and reuse easier
 * `traces` - Classes used by `simulation` to represent time-series. (Ideally this will be moved to neo)
 * `stdimports` - A package used to import everything. (``from morphforge.stdimports import *``)

and `morphforgecontrib` contains

 * `data_library` - a repository of standard models. (eg Hodgkin-Huxley 52)
 * `tags` - Functions for automatically tagging.



Plugins
~~~~~~~

morphforge extensively uses a plugin architecture. Although making the 
architecture slightly more complex; it means it is possible to write your own
specialised channel types, synapse models and stimuli, for different simulators
backends. Typically, plugins are registered globally at the beginning of a 
simulation via module imports. 

Packages
========


Morphology
~~~~~~~~~~~~~~~~

The morphology layer provides object models for loading, saving, traversing, 
maniulating and visualing neuronal morphologies.  A variety of formats are 
supported (swc, channelml) are supported and it is simple to add additional
importers and exporters. Visualisation is possible via MayaVi and matplotlib.
For more information on morphologies, see XX.

Simulation
~~~~~~~~~~~~~~~~

The simulation layer provides the core API for simulator independant
simulation, defining basic types such as cells, channels, stimuli, synapses, and 
gap-junctions, and providing infrastructure for recording  various values from 
simuations. It provides the infrastructure to make it very easy to switch between
different backends.
For more information on simulations, see XX.


Simulation Analysis
~~~~~~~~~~~~~~~~~~~~

The simulation analysis layer provides tools for processing and visualising the
results of simulations, such as finding spikes, and plotting graphs.
A workhorse of this modules is the TagViewer. This class makes it very simple
to visualise various variables in a network, without lots of boilorplate code.


=======
Package Overview
================

Morphforge is a large package; it has been split into
2 main packages:

 * `morphforge` contains the core object API for the object models.
 * `morphforgecontrib` contains 'data' code, for example, the definitions of 
   channel and synapse types.

Morphforge has 4 main layers:
  * `core` 
  * `morphology`
  * `simulation`
  * `simulation analysis`

which build on top of each other. You can use the `morphology` layer to work with 
morphologies with no knowledge of the `simulation` layer. However, the `simulation`
layer references both the `core` and `morphology` layers.  Both `morphforge` and `morphforgecontrib` have similar directories, reflecting
these layers. 

morphforge also contains the following directories:

 * `constants` - Defines some common constants
 * `componentlibraries` - Infrastructure to make component tracking and reuse easier
 * `traces` - Classes used by `simulation` to represent time-series. (Ideally this will be moved to neo)
 * `stdimports` - A package used to import everything. (``from morphforge.stdimports import *``)

and `morphforgecontrib` contains

 * `data_library` - a repository of standard models. (eg Hodgkin-Huxley 52)
 * `tags` - Functions for automatically tagging.



Plugins
=======

morphforge extensively uses a plugin architecture. Although making the 
architecture slightly more complex; it means it is possible to write your own
specialised channel types, synapse models and stimuli, for different simulators
backends. Typically, plugins are registered globally at the beginning of a 
simulation via module imports. 


Morphology
==========

The morphology layer provides object models for loading, saving, traversing, 
maniulating and visualing neuronal morphologies.  A variety of formats are 
supported (swc, channelml) are supported and it is simple to add additional
importers and exporters. Visualisation is possible via MayaVi and matplotlib.
For more information on morphologies, see XX.

Simulation
==========

The simulation layer provides the core API for simulator independant
simulation, defining basic types such as cells, channels, stimuli, synapses, and 
gap-junctions, and providing infrastructure for recording  various values from 
simuations. It provides the infrastructure to make it very easy to switch between
different backends.
For more information on simulations, see XX.


Simulation Analysis
====================

The simulation analysis layer provides tools for processing and visualising the
results of simulations, such as finding spikes, and plotting graphs.
A workhorse of this modules is the TagViewer. This class makes it very simple
to visualise various variables in a network, without lots of boilorplate code.


>>>>>>> d25b786a83994b945959dfd2b6ceeb9d0b08af89
For more information on simulation analysis, see XX.



