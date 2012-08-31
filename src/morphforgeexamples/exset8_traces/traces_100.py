
import morphforge.stdimports as mf
from  morphforge.traces.generation  import TraceStringParser
import quantities as pq


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
    (mf.TraceFixedDT, lambda tr: tr.convert_to_fixed(dt=0.1*pq.ms) ),
    #(mf.TraceVariableDT, lambda tr: tr.convert_to_variable(eps=0.1) ),
    (mf.TracePiecewise, lambda tr: tr.convert_to_piecewise() ),
        ]


returning_trace_methods = [
        ('filterbessel', lambda tr: tr.filterbessel(filterorder=8, cutoff_frequency=5*pq.Hz) ),
        ('filterlowpassrc', lambda tr: tr.filterlowpassrc(tau=2*pq.ms) ),
        ('shift', lambda tr: tr.shift(offset=100*pq.ms)),

        ('convert_to_fixed', lambda tr: tr.convert_to_fixed(dt=0.1*pq.ms) ),
        #('convert_to_piecewise', lambda tr: tr.convert_to_piecewise() ),
        ]  






tr = TraceStringParser.Parse(tests[0])
print tr.get_min_time()
print tr.clone().get_min_time()

#sys.exit(0)


for t in tests:

    tr = TraceStringParser.Parse(t)

    for (method_name, method_functor) in returning_trace_methods:

        f = QuantitiesFigure()
        f.suptitle('Testing Method: %s'%method_name)
        ax1 = f.add_subplot(211)
        ax2 = f.add_subplot(212)

        ax1.plotTrace(tr, label='Original')

        for (conv_type, conv_functor) in conversions:
            #try:
            tr_new = conv_functor(tr)
            #except AttributeError:
            #    continue

            if not mf.TraceMethodCtrl.has_method(conv_type, method_name):
                continue
            ax2.plotTrace(method_functor(tr_new), label='%s:%s' % (conv_type.__name__, method_name) )


        ax1.legend()
        ax2.legend()




import pylab
pylab.show()







