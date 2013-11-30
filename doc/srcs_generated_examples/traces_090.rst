
.. _example_traces_090:

Example 24. <Missing Docstring>
===============================




Code
~~~~

.. code-block:: python

    
    import morphforge.stdimports as mf
    from  morphforge.traces.generation  import TraceStringParser
    from morphforge import units
    
    from mhlibs.quantities_plot import QuantitiesFigure
    
    t = """{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 130ms THEN FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms"""
    
    tr = TraceStringParser.Parse(t)
    
    
    trFix = tr.convert_to_fixed(dt=01.*units.ms)
    
    print 't1:', tr.integrate()
    print 't2:', trFix.integrate()
    
    f = QuantitiesFigure()
    ax1 = f.add_subplot(211)
    ax2 = f.add_subplot(212)
    
    
    trFixSquared = trFix ** 2
    print trFixSquared.integrate()
    
    print (tr**2).integrate()
    
    
    ax1.plotTrace(trFix)
    ax2.plotTrace(trFixSquared)
    
    
    
    
    
    
    
    import pylab
    pylab.show()
    
    
    
    
    
    
    
    








Output
~~~~~~

.. code-block:: bash

        




