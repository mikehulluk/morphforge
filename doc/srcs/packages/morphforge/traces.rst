morphforge.traces
============================

.. automodule:: morphforge.traces
    :no-members:



morphforge.traces.tracetypes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: morphforge.traces.tracetypes
    :no-members:

.. autosummary::
   
    morphforge.traces.tracetypes.Trace
    morphforge.traces.tracetypes.TracePointBased
    morphforge.traces.tracetypes.TraceFixedDT
    morphforge.traces.tracetypes.TraceVariableDT
    morphforge.traces.tracetypes.TracePiecewise

    morphforge.traces.tracetypes.PieceWiseComponentVisitor
    morphforge.traces.tracetypes.TracePieceFunction
    morphforge.traces.tracetypes.TracePieceFunctionLinear
    morphforge.traces.tracetypes.TracePieceFunctionFlat

    

morphforge.traces.traceobjpluginctrl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: morphforge.traces.traceobjpluginctrl
    :no-members:

.. autosummary::

    morphforge.traces.traceobjpluginctrl.TraceMethodCtrl
    morphforge.traces.traceobjpluginctrl.TraceOperatorCtrl



morphforge.traces.operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: morphforge.traces.operators
    :no-members:

.. autosummary::
    


    morphforge.traces.operators.TraceOperator_TraceFixedDT_TraceFixedDT
    morphforge.traces.operators.TraceOperator_TraceFixedDT_Quantity
    morphforge.traces.operators.TraceOperator_TraceFixedDT_Scalar
    morphforge.traces.operators.TraceOperator_TraceVariableDT_Quantity
    morphforge.traces.operators.TraceOperator_TraceVariableDT_Scalar
    morphforge.traces.operators.PiecewiseScalarOperation
    morphforge.traces.operators.TraceOperator_TracePiecewise_Quantity
    morphforge.traces.operators.variable_dt_rebasing.VariableDTRebaseTimeValues



morphforge.traces.methods
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: morphforge.traces.methods
    :no-members:

.. autosummary::

    morphforge.traces.methods.TraceConverter
    morphforge.traces.methods.TraceApproximator
    
    





morphforge.traces.eventset
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: morphforge.traces.eventset
    :no-members:

.. autosummary::

    morphforge.traces.eventset.Event
    morphforge.traces.eventset.EventSet


morphforge.traces.generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: morphforge.traces.generation
    :no-members:

.. autosummary::

    morphforge.traces.generation.TraceStringParser
    morphforge.traces.generation.TraceGeneratorParserLexer
    morphforge.traces.generation.FunctionPrototype


morphforge.traces.io
~~~~~~~~~~~~~~~~~~~~

.. automodule:: morphforge.traces.io
    :no-members:

.. autosummary::

    morphforge.traces.io.InvalidNeuroCSVFile
    morphforge.traces.io.NeuroCSVHeaderData
    morphforge.traces.io.NeuroCSVParser
    morphforge.traces.io.NeuroCSVWriter
    morphforge.traces.io.TraceLoader


morphforge.traces.tags
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: morphforge.traces.tags
    :no-members:

.. autosummary::

    morphforge.traces.tags.TagSelector
    morphforge.traces.tags.TagSelectorAny
    morphforge.traces.tags.TagSelectorAll
    morphforge.traces.tags.TagSelectorBinary
    morphforge.traces.tags.TagSelectorOr
    morphforge.traces.tags.TagSelectorAnd
    morphforge.traces.tags.TagSelectorNot
    morphforge.traces.tags.TagSelect

