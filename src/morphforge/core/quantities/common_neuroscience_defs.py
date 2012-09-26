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

import quantities as pq

# Conductances:
mS = pq.UnitQuantity('milli-Siemen', pq.milli * pq.siemens, symbol='mS')
uS = pq.UnitQuantity('micro-Siemen', pq.micro * pq.siemens, symbol='uS')
nS = pq.UnitQuantity('nano-Siemen', pq.nano * pq.siemens, symbol='nS')
pS = pq.UnitQuantity('pico-Siemen', pq.pico * pq.siemens, symbol='pS')

# Capacitances:
mF = pq.UnitQuantity('millifarad', pq.milli * pq.farad, symbol='mF')
uF = pq.UnitQuantity('microfarad', pq.micro * pq.farad, symbol='uF')
nF = pq.UnitQuantity('nanofarad', pq.nano * pq.farad, symbol='nF')
pF = pq.UnitQuantity('picofarad', pq.pico * pq.farad, symbol='pF')

# Areas:
um2 = pq.UnitQuantity('micrometer-squared', pq.um ** 2, symbol='um2')
cm2 = pq.UnitQuantity('centimeter-squared', pq.cm ** 2, symbol='cm2')
mm2 = pq.UnitQuantity('micrometer-squared', pq.mm ** 2, symbol='mm2')
m2 = pq.UnitQuantity('meter-squared', pq.m ** 2, symbol='m2')

areas = [m2, cm2, mm2, um2]

currents = [pq.amp, pq.milliamp, pq.microampere, pq.nanoamp, pq.picoamp]
conductances = [pq.S, mS, uS, nS, pS]
capacitances = [pq.F, mF, uF, nF, pF]

# Create the possible densities:
for a in areas:
    for i in currents:
        pq.UnitQuantity('%s per %s' % (i.name, a.name), 
                        i / a,
                        symbol='%s/%s' % (i, a))

    for g in conductances:
        pq.UnitQuantity('%s per %s' % (g.name, a.name), 
                        g / a,
                        symbol='%s/%s' % (g, a))

    for c in capacitances:
        pq.UnitQuantity('%s per %s' % (c.name, a.name), 
                        c / a,
                        symbol='%s/%s' % (c, a))

## Molar Quanities:
# http://en.wikipedia.org/wiki/Mole_(unit)#Related_units
Molar = pq.UnitQuantity('Mol', pq.mol / pq.liter)
nMolar = pq.UnitQuantity('nMol', pq.nano * Molar, symbol='nMolar')
uMolar = pq.UnitQuantity('uMol', pq.micro * Molar, symbol='uMolar')

# Specials:
ohmcm = pq.UnitQuantity('ohmcm', pq.ohm * pq.centimeter, symbol='ohmcm')
MOhm = pq.UnitQuantity('megaOhm', pq.ohm * pq.mega, symbol='MOhm')

mV = pq.milli * pq.volt

# HACK to get old scripts working again!
pA_um2 = pq.pico * pq.amp / um2




