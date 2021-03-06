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
    RANGE gtot
    RANGE popening
    RANGE voltage_dependancy
    RANGE is_vdep_on
    RANGE peak_conductance

    RANGE eta
    RANGE mg2conc
    RANGE gamma


    RANGE is_conductance_limited_on
    RANGE conductance_limit
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
    peak_conductance = -100000 (uS)

    is_conductance_limited_on = -1
    conductance_limit = -1

    eta = 0.1
    mg2conc=0.5
    gamma=0.08 (/mV)

}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    gtot (uS)
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


FUNCTION vdep_func(Vin(mV), vdep)
{
    if(vdep<0.5){
        vdep_func = 1.0
    }
    else {
         vdep_func = (1. / (1.+ eta*mg2conc*exp(-gamma*Vin)))
    }
}


BREAKPOINT {
    SOLVE state METHOD cnexp
    voltage_dependancy = vdep_func(v, is_vdep_on)
    g = (B - A)
    gtot = g*voltage_dependancy
    i = gtot*(v - e)

}

DERIVATIVE state {
    A' = -A/tau1
    B' = -B/tau2
}

NET_RECEIVE(weight (uS)) {
    LOCAL clip, sv_max


    VERBATIM
    float x = ((float) rand()) /  RAND_MAX;
    if(x < popening)
    {
    ENDVERBATIM
        weight = 1.0

        A = A + weight*factor * peak_conductance
        B = B + weight*factor * peak_conductance


        if(is_conductance_limited_on> 0.5)
        {
            sv_max = weight*factor * peak_conductance * conductance_limit

            if(A>sv_max) {A=sv_max}
            if(B>sv_max) {B=sv_max}



        }


        ://clip = weight*factor *3000 * peak_conductance
        ://if(A>clip) {A=clip}
        ://if(B>clip) {B=clip}

    VERBATIM
    }
    ENDVERBATIM


}

"""


    seed_val = (mfrandom.MFRandom._seed if mfrandom.MFRandom._seed
                is not None else 0)
    comment_val = ('//' if mfrandom.MFRandom._seed is not None else '')
    return x.replace('$randomseed', '%d' % seed_val).replace('$COMMENT'
            , comment_val)


