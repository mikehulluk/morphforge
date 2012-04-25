


import morphforge.stdimports as mf
from mhlibs.quantities_plot import QuantitiesFigure
import pylab

from morphforge.stdimports import unit, reduce_to_variable_dt_trace


t1 = mf.TraceGenerator.generate_flat(value='1:mV')
#t2 = mf.TraceGenerator.generate_flat(value='0.0015:V')
t2 = mf.TraceGenerator.generate_ramp(value_start='0.0015:V', value_stop='2.5:mV', npoints=20)



f = QuantitiesFigure()
ax = f.add_subplot(111)
ax.plotTrace(t1, marker='x')
ax.plotTrace(t2, marker='o')
ax.plotTrace(t1+t2, marker='<')
ax.plotTrace((t2+t2)*3.0+unit('0.03:V'), marker='<')

t1 = mf.fixed_to_variable_dt_trace(t1, '0.01:mV')
ax.plotTrace(t1, marker='>')
ax.legend()

pylab.show()

