======================
Morphforge Users Guide
======================


.. contents::
  
Package Overview
++++++++++++++++

.. toctree::
    :maxdepth: 1
    
    /srcs/packages/package_overview
    

morphforge
++++++++++++

Key Concepts
------------

.. toctree::
    :maxdepth: 2
    
    /srcs/concepts/morphology.rst
    /srcs/concepts/simulation.rst
    /srcs/concepts/simulationanalysis.rst

*~/.morphforgerc* configuration
--------------------------------

.. toctree::
    
    /srcs/morphforgerc
    


[Package List]
--------------------

.. toctree::
   :maxdepth: 2

   /srcs/packages/morphforge/core.rst
   /srcs/packages/morphforge/morphology.rst
   /srcs/packages/morphforge/simulation.rst
   /srcs/packages/morphforge/simulationanalysis.rst
   
.. toctree::
   :maxdepth: 1
   
   /srcs/packages/morphforge/traces.rst
   /srcs/packages/morphforge/componentlibraries.rst
   /srcs/packages/morphforge/constants.rst










morphforgecontrib
+++++++++++++++++


Plugins
-------

Morphology-Formats
~~~~~~~~~~~~~~~~~~
Morphforge can load the following morphology formats. If you would like to use
a format not listed here, `why not contribute it <somelink>`_ ?


=============== ================================ ========================================== ===================
Format          Command                          Details                                    Examples
=============== ================================ ========================================== ===================
.swc            MorphologyTree.from_swc()        For more control, and loading multiple     See simXX
                MorphologyArray.from_swc()       morphologies from a single file, see XX.
--------------- -------------------------------- ------------------------------------------ -------------------
morphml         MorphologyTree.from_swc()        MH TO CHECK AND STANDARDISE!
--------------- -------------------------------- ------------------------------------------ -------------------
.hdf            .... etc....
=============== ================================ ========================================== ===================



=============== ================================ ========================================== ===================
Format          Command                          Details                                    Examples
=============== ================================ ========================================== ===================
.swc            MorphologyTree.to_swc()          For more control, and loading multiple     See simXX
                MorphologyArray.to_swc()         morphologies from a single file, see XX.
--------------- -------------------------------- ------------------------------------------ -------------------
morphml         MorphologyTree.to_swc()          MH TO CHECK AND STANDARDISE!
--------------- -------------------------------- ------------------------------------------ -------------------
.hdf            .... etc....
=============== ================================ ========================================== ===================



Channel-Formats
~~~~~~~~~~~~~~~

========================================================================================================================================================= ========== ============ ========================================== ===================
Channel-Type                                                                                                                                              <NEURON>   <Summary>    Details                                    Examples                            
========================================================================================================================================================= ========== ============ ========================================== ===================
:py:class:`~morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core.SimulatorSpecificChannel`                                               X          X            dskfsdf  
:py:class:`~morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core.BuiltinChannel`                                             X          X            sdfsdf
--------------------------------------------------------------------------------------------------------------------------------------------------------- ---------- ------------ ------------------------------------------ -------------------
:py:class:`~morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta.MM_AlphaBetaChannel`
:py:class:`~morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabetabeta.MM_AlphaBetaBetaChannel`
:py:class:`~morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak.MM_LeakChannel`
--------------------------------------------------------------------------------------------------------------------------------------------------------- ---------- ------------ ------------------------------------------ -------------------
:py:class:`~morphforgecontrib.simulation.membranemechanisms.inftauinterpolated.core.MM_InfTauInterpolatedChannel`
:py:class:`~morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core.NeuroML_Via_NeuroUnits_Channel`
:py:class:`~morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_core.NeuroML_Via_XSL_Channel`
:py:class:`~morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge.NeuroUnitEqnsetMechanism`
========================================================================================================================================================= ========== ============ ========================================== ===================




Synapse-Presynaptic Triggers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========================================================================================================================================================= ========== ============ ========================================== ===================
Pre-Synaptic Trigger                                                                                                                                      <NEURON>   <Summary>    Details                                    Examples                            
========================================================================================================================================================= ========== ============ ========================================== ===================
:py:class:`~morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms.PreSynapticMech_VoltageThreshold`                                            X          X            dskfsdf  
--------------------------------------------------------------------------------------------------------------------------------------------------------- ---------- ------------ ------------------------------------------ -------------------
:py:class:`~morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms.PreSynapticMech_TimeList`                                                    X          X            sdfsdf
========================================================================================================================================================= ========== ============ ========================================== ===================



Synapse-Postynaptic Mechanisms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========================================================================================================================================================= ========== ============ ========================================== ===================
Post-Synaptic Mechanism                                                                                                                                   <NEURON>   <Summary>    Details                                    Examples          
========================================================================================================================================================= ========== ============ ========================================== ===================
:py:class:`~morphforgecontrib.simulation.synapses.core.postsynaptic_mechanisms.PostSynapticMech_ExpSyn`                                                   X          X            dskfsdf  
:py:class:`~morphforgecontrib.simulation.synapses.core.postsynaptic_mechanisms.PostSynapticMech_Exp2Syn`                                                  X          X            sdfsdf
:py:class:`~morphforgecontrib.simulation.synapses.core.postsynaptic_mechanisms.PostSynapticMech_Exp2SynNMDA`                                              X          X            sdfsdf
:py:class:`~morphforgecontrib.simulation.synapses_neurounit.NeuroUnitEqnsetPostSynaptic`                                                                  X          X            sdfsdf
========================================================================================================================================================= ========== ============ ========================================== ===================



Current Clamp protocols
~~~~~~~~~~~~~~~~~~~~~~~~

========================================================================================================================================================= ========== ============ ========================================== ===================
Post-Synaptic Mechanism                                                                                                                                   <NEURON>   <Summary>    Details                                    Examples          
========================================================================================================================================================= ========== ============ ========================================== ===================
:py:class:`~morphforge.simulation.base.stimulation.CurrentClampStepChange`                                                                                X          X            dskfsdf  
:py:class:`~morphforgecontrib.simulation.stimulation.currentclamps.sinwave.currentclamp_sinwave_core.CurrentClamp_SinWave`                                X          X            sdfsdf
========================================================================================================================================================= ========== ============ ========================================== ===================

Voltage Clamp protocols
~~~~~~~~~~~~~~~~~~~~~~~~

========================================================================================================================================================= ========== ============ ========================================== ===================
Post-Synaptic Mechanism                                                                                                                                   <NEURON>   <Summary>    Details                                    Examples          
========================================================================================================================================================= ========== ============ ========================================== ===================
:py:class:`~morphforge.simulation.base.stimulation.VoltageClampStepChange`                                                                                X          X            dskfsdf  
========================================================================================================================================================= ========== ============ ========================================== ===================






Models
------
HH model


Channels 
~~~~~~~~~


========================================= ================== ==============================
Model Source                              Channel Type       Key
========================================= ================== ==============================
HH-52                                     Na                 (??)
HH-52                                     K                  (??)
HH-52                                     Lk                 (??)
========================================= ================== ==============================






Cells
~~~~~



[Package List]
---------------------------

.. toctree::
   :maxdepth: 2









   


Test Suites
++++++++++++

.. toctree::
   :maxdepth: 3

   /srcs/tests/morphforgetest




Complete Class List
++++++++++++++++++++

.. toctree::
    :maxdepth: 2
    
    /srcs/packages/complete_class_list.rst
    

Indices and tables
++++++++++++++++++++++++

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
















