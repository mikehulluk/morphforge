Simulation Layer
================

.. comment::
    # Run this:
    cd /local/scratch/mh735/hw/morphforge
    grep -l 'StdChlAlphaBetaBeta' doc/srcs_generated_examples/*.rst | sed 's;doc/srcs_generated_examples/;  * :ref:`example_;g' | sed 's/$/`/g' 



Morphforge-contrib defines the following types of objects:


.. contents:: mf-types
    :depth: 2
    





.. _section_mfchanneltypes:

Channel-Types
-------------

StdChlLeak
~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.hh_style.core.mmleak.StdChlLeak` is a leak channel consisting of a constant reversal potential and conductance density.


.. seealso::


    * :ref:`example_singlecell_simulation010`
    * :ref:`example_singlecell_simulation020`
    * :ref:`example_singlecell_simulation030`
    * :ref:`example_singlecell_simulation040`
    * :ref:`example_singlecell_simulation060`
    * :ref:`example_singlecell_simulation065`
    * :ref:`example_singlecell_simulation090`
    * :ref:`example_assorted_10compareHHChls`

    

StdChlAlphaBeta
~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta.StdChlAlphaBeta` is a Hodgkin-Huxley type channel that can be constructed directly in Python. The form of the rate constants are:

.. math::

    \alpha(V),\beta(V) = \frac{ A+BV}{ C+ exp( (D+V)/E) }

where A,B,C,D & E are constants.

.. seealso::

    * :ref:`example_singlecell_simulation020`
    * :ref:`example_singlecell_simulation030`
    * :ref:`example_singlecell_simulation040`
    * :ref:`example_singlecell_simulation060`
    * :ref:`example_singlecell_simulation065`
    * :ref:`example_assorted_10compareHHChls`



StdChlAlphaBetaBeta
~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.hh_style.core.mmalphabetabeta.StdChlAlphaBetaBeta` is similar to StdChlAlphaBeta, except that different forms for :math:`\beta` can be used for different values for V. (See for example Dale-95)


SimulatorSpecificChannel
~~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.exisitingmodfile.core.SimulatorSpecificChannel` also MODL code to be use directly within with a NEURON simulation.



NeuroUnits
~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.neurounits.neuro_units_bridge.NeuroUnitEqnsetMechanism` allows channels specified in NeuroUnits as strings to be used in morphforge

.. seealso::

  * :ref:`example_assorted_10compareHHChls`
  * :ref:`example_poster1`



NeuroML_Via_XSL_Channel
~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.neuroml_via_xsl.neuroml_via_xsl_core.NeuroML_Via_XSL_Channel` allows channels specified in NeuroUnits as strings to be used in morphforge.

.. seealso::

  * :ref:`example_assorted_10compareHHChls`



NeuroML_Via_NeuroUnits_Channel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.channels.neuroml_via_neurounits.neuroml_via_neurounits_core.NeuroML_Via_NeuroUnits_Channel` is for internal use for testing a conversion from NeuroML to Neurounits to ensure they give the same simulation results.

.. seealso::

  * :ref:`example_assorted_10compareHHChls`




PreSynapticTrigger-Types
-------------------------

SynapticTriggerAtTimes
~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforge.simulation.base.synaptictriggers.SynapticTriggerAtTimes` causes PostSynaptic objects to be triggered at specific times.


SynapticTriggerByVoltageThreshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforge.simulation.base.synaptictriggers.SynapticTriggerByVoltageThreshold` causes PostSynaptic objects to be triggered when the voltage at a presynaptic location crosses a particular threshold.




PostSynapticTemplate-Types
--------------------------


.. todo::

    THIS!
    

NeuroUnits
~~~~~~~~~~

PostSynapticMech_ExpSyn_Base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.synapse_templates.exponential_form.expsyn.core.PostSynapticMech_ExpSyn_Base`


PostSynapticMech_Exp2Syn_Base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base`



PostSynapticMech_Exp2SynNMDA_Base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base`



Stimuli-Types
--------------

CurrentClampStepChange
~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforge.simulation.base.stimulation.CurrentClampStepChange`

CurrentClampSinwave
~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforgecontrib.simulation.stimulation.currentclamps.sinwave.currentclamp_sinwave_core.CurrentClampSinwave`

VoltageClampStepChange
~~~~~~~~~~~~~~~~~~~~~~
:py:class:`~morphforge.simulation.base.stimulation.VoltageClampStepChange`

