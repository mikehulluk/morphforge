#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

from morphforge.core import mfrandom
import random


def getExp2SynModfile():

    x = """
COMMENT



MODIFIED BY MIKE HULL, TO ALLOW FOR STOCHASITIC TRANSMISSION

ENDCOMMENT



VERBATIM
#include <stdlib.h>

ENDVERBATIM




NEURON {
    POINT_PROCESS Exp2SynMorphforge
    RANGE tau1, tau2, e, i
    NONSPECIFIC_CURRENT i

    RANGE g
    RANGE popening
    RANGE peak_conductance
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    tau1= 1.5 (ms) <1e-9,1e9>
    tau2 = 12.0 (ms) <1e-9,1e9>
    e=0    (mV)
    popening=1.0 () <0.0,1.0>
    peak_conductance = -100000 (uS)
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor
}

STATE {
    A (uS)
    B (uS)
}

INITIAL {
    LOCAL tp
    if (tau1/tau2 > .9999) {
        tau1 = .9999*tau2
    }
    A = 0
    B = 0
    tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
    factor = -exp(-tp/tau1) + exp(-tp/tau2)
    factor = 1/factor



    VERBATIM
    {
       $COMMENT srand($randomseed);
    }
    ENDVERBATIM

}

BREAKPOINT {
    SOLVE state METHOD cnexp
    g = B - A
    i = g*(v - e)
}

DERIVATIVE state {
    A' = -A/tau1
    B' = -B/tau2
}

NET_RECEIVE(weight (uS)) {


VERBATIM
float x = ((float) rand()) /  RAND_MAX;
if(x < popening) {
ENDVERBATIM

    weight = 1.0    
    A = A + weight*factor*peak_conductance
    B = B + weight*factor*peak_conductance
    
VERBATIM
}
ENDVERBATIM


}

"""
#    assert mfrandom.MFRandom._seed == 0

    seedVal = (mfrandom.MFRandom._seed if mfrandom.MFRandom._seed
               is not None else 0)
    commentVal = ('//' if mfrandom.MFRandom._seed is not None else '')
    return x.replace('$randomseed', '%d' % seedVal).replace('$COMMENT',
            commentVal)


