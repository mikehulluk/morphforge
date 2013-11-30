
.. _example_traces_100:

Example 25. <Missing Docstring>
===============================




Code
~~~~

.. code-block:: python

    
    import morphforge.stdimports as mf
    from  morphforge.traces.generation  import TraceStringParser
    from morphforge import units
    
    
    import mredoc as mrd
    
    tests = [
    #"""{d:pA} AT 0ms FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 120ms THEN FLAT(50) FOR 20ms """,
    #"""{d:pA} AT 0ms FLAT(0) UNTIL 150ms THEN FLAT(120) FOR 20ms THEN FLAT(0) FOR 20ms""",
    #"""{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 160ms""",
    """{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 130ms THEN FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms""",
    #"""{d:pA} FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms""",
     ]
    
    
    
    from mhlibs.quantities_plot import QuantitiesFigure
    
    
    
    returning_quantities = [
        ('mean', lambda tr: tr.mean()),
        ('min', lambda tr: tr.min()),
        ('max', lambda tr: tr.max())
    
    ]
    
    conversions = [
        (mf.TraceFixedDT, lambda tr: tr.convert_to_fixed(dt=0.1*units.ms) ),
        #(mf.TraceVariableDT, lambda tr: tr.convert_to_variable(eps=0.1) ),
        (mf.TracePiecewise, lambda tr: tr.convert_to_piecewise() ),
            ]
    
    
    returning_trace_methods = [
            ('filterbessel', lambda tr: tr.filterbessel(filterorder=8, cutoff_frequency=1000*units.Hz) ),
            ('filterbutterworth', lambda tr: tr.filterbutterworth(filterorder=8, cutoff_frequency=1000*units.Hz) ),
            ('filterlowpassrc', lambda tr: tr.filterlowpassrc(tau=2*units.ms) ),
    
            ('shift', lambda tr: tr.shift(offset=100*units.ms)),
            ('window', lambda tr: tr.window((75*units.ms, 160*units.ms)) ),
            ('windowshift', lambda tr: tr.windowshift((75*units.ms, 160*units.ms)) ),
    
            ('convert_to_fixed', lambda tr: tr.convert_to_fixed(dt=0.1*units.ms) ),
            ('convert_to_piecewise', lambda tr: tr.convert_to_piecewise() ),
            ]  
    
    
    
    
    
    
    tr = TraceStringParser.Parse(tests[0])
    print tr.get_min_time()
    print tr.clone().get_min_time()
    
    #sys.exit(0)
    
    
    
    def test_trace_method_traceout(src_trace, method_name, method_functor):
        f = QuantitiesFigure(figsize=(6,4))
        f.suptitle('Testing Method: %s'%method_name)
        ax1 = f.add_subplot(211)
        ax2 = f.add_subplot(212)
    
        ax1.plotTrace(src_trace, label='Original')
    
        for (conv_type, conv_functor) in conversions:
            tr_new = conv_functor(src_trace)
    
            if not mf.TraceMethodCtrl.has_method(conv_type, method_name):
                continue
            ax2.plotTrace(method_functor(tr_new), label='%s:%s' % (conv_type.__name__, method_name) )
    
        ax1.legend()
        ax2.legend()
    
        return mrd.Section(
                'Test: %s'%method_name,
                mrd.Image(f.fig, auto_adjust=False)
                )
    
    
    def test_trace_method_scalarout(src_trace, method_name, method_functor):
    
        res =[]
        for (conv_type, conv_functor) in conversions:
            tr_new = conv_functor(src_trace)
    
            if not mf.TraceMethodCtrl.has_method(conv_type, method_name):
                res.append([conv_type.__name__, '--'])
                continue
            
            else:
                res_new = method_functor(tr_new)
                res.append([conv_type.__name__, str(res_new)])
            #ax2.plotTrace(method_functor(tr_new), label='%s:%s' % (conv_type.__name__, method_name) )
    
        
        print res
        (header,data) = zip(*res)
        print 'header', header
        print 'data', data
        return mrd.Section('Tesing Method: %s'%method_name,
                mrd.VerticalColTable(header,[data])
                )
    
    
    for t in tests:
    
        tr = TraceStringParser.Parse(t)
    
    
        sects = []
        for (method_name, method_functor) in returning_trace_methods:
            s = test_trace_method_traceout(tr, method_name, method_functor)
            sects.append(s)
    
        #returning_quantities = [
        #('mean', lambda tr: tr.mean()),
    
    
        
    
        for (method_name, method_functor) in returning_quantities:
            s = test_trace_method_scalarout(tr, method_name, method_functor)
            sects.append(s) 
    
    
        mrd.Section('Testing: %s'%t, sects).to_pdf('~/Desktop/trace_testing.pdf')
    
    
    
    
    
    
    
    #import pylab
    #pylab.show()
    
    
    
    
    
    
    
    








Output
~~~~~~

.. code-block:: bash

        




