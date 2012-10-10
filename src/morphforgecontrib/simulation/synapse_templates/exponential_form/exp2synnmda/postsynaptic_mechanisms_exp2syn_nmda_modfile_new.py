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





def get_exp2_syn_nmda_modfile():

    x = """
COMMENT
Two state kinetic scheme synapse described by rise time tau1,
and decay time constant tau2. The normalized peak condunductance is 1.
Decay time MUST be greater than rise time.

The solution of A->G->bath with rate constants 1/tau1 and 1/tau2 is
 A = a*exp(-t/tau1) and
 G = a*tau2/(tau2-tau1)*(-exp(-t/tau1) + exp(-t/tau2))
    where tau1 < tau2

If tau2-tau1 -> 0 then we have a alphasynapse.
and if tau1 -> 0 then we have just single exponential decay.

The factor is evaluated in the
initial block such that an event of weight 1 generates a
peak conductance of 1.

Because the solution is a sum of exponentials, the
coupled equations can be solved as a pair of independent equations
by the more efficient cnexp method.


MODIFIED BY MIKE HULL, TO ALLOW FOR STOCHASITIC TRANSMISSION

ENDCOMMENT



VERBATIM
#include <stdlib.h>
ENDVERBATIM




NEURON {
    POINT_PROCESS Exp2SynNMDAMorphforge
    RANGE tau1, tau2, e, i
    NONSPECIFIC_CURRENT i

    RANGE g
    RANGE popening
    RANGE voltage_dependancy
    RANGE is_vdep_on
    RANGE peak_conductance
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    tau1=.1 (ms) <1e-9, 1e9>
    tau2 = 10 (ms) <1e-9, 1e9>
    e=0    (mV)
    popening=1.0 () <0.0, 1.0>
    is_vdep_on = 1
    peak_conductance = -100000 ()
        
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor
    voltage_dependancy
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


FUNCTION vdep_func(Vin, vdep)
{
    if(vdep<0.5){
        vdep_func = 1.0
    }
    else {
         vdep_func = (1. / (1.+ 0.1*0.5*exp(-0.08*Vin)))
    }
}


BREAKPOINT {
    SOLVE state METHOD cnexp
    voltage_dependancy = vdep_func(v, is_vdep_on)
    g = (B - A) 
    i = g*(v - e) * voltage_dependancy

}

DERIVATIVE state {
    A' = -A/tau1
    B' = -B/tau2
}

NET_RECEIVE(weight (uS)) {
    LOCAL clip
    VERBATIM
    float x = ((float) rand()) /  RAND_MAX;
    if(x < popening)
    {
        //printf("%f %f", A, B);
    ENDVERBATIM
        weight = 1.0

        A = A + weight*factor * peak_conductance
        B = B + weight*factor * peak_conductance

        clip = weight*factor *3000 * peak_conductance
        if(A>clip) {A=clip}
        if(B>clip) {B=clip}

    VERBATIM
        //printf("->%f %f (%f)\\n", A, B, _lclip);
    }
    ENDVERBATIM


}

"""


    seed_val = (mfrandom.MFRandom._seed if mfrandom.MFRandom._seed
                is not None else 0)
    comment_val = ('//' if mfrandom.MFRandom._seed is not None else '')
    return x.replace('$randomseed', '%d' % seed_val).replace('$COMMENT'
            , comment_val)


