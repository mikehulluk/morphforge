

_mod_txt = """
NEURON {
	POINT_PROCESS ExpSynMorphforge
	RANGE tau, e, i
	NONSPECIFIC_CURRENT i
    
    RANGE peak_conductance
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	tau = 0.1 (ms) <1e-9,1e9>
	e = 0	(mV)
    peak_conductance = -100000 ()
}

ASSIGNED {
	v (mV)
	i (nA)
}

STATE {
	g (uS)
}

INITIAL {
	g=0
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	i = g*(v - e)
}

DERIVATIVE state {
	g' = -g/tau
}

UNITSOFF
NET_RECEIVE(weight (uS)) {
    weight = 1.0
	g = g + weight * peak_conductance
}
UNITSON
"""

def getExpSynModfile():
    return _mod_txt
