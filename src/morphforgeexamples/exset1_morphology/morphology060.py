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



"""Simple morphology analysis

In this script, we load in an .swc which has 2 regions; "apicaldendrite"
and "dendrite" declared in its .swc file, then look at its surface area, and how
the radius of the region types becomes smaller as we move away from the soma.

.. warning::

    I have not written tests for the surface area and volume functions,
    so don't trust them yet!  This is proof of concept code!

"""
import morphforge.stdimports as mf
import pylab

# Load a morphology from an SWC File, and look at the surface area and
# volume of the different section types
testSrcsPath = mf.LocMgr().get_test_srcs_path()
srcSWCFile = mf.Join(testSrcsPath, "swc_files/28o_spindle20aFI.CNG.swc")
morph = mf.MorphologyTree.fromSWC(src=open(srcSWCFile))


#Look at the regions that are used in this morphology:
for region in  morph.get_regions():
    #print region
    print "Region: %s (%d)"%(region.name, 0)# len(region))
    print " - Surface Area: ", sum([section.area for section in region]), "um2"
    print " - Volume: ", sum([section.volume for section in region]), "um3"




# (Simple, but not the most efficient way to
# to this. For illustration purposes:)

def section_dist_to_dummy(sect):
    if sect.is_dummy_section(): return 0.0
    return section_dist_to_dummy(sect.parent) + sect.get_length()

f = pylab.figure()

ax1 = f.add_subplot("111")
ax1.set_xlabel("Distance from soma")
ax1.set_ylabel("Radius")
ax1.set_color_cycle(['red','blue'])
for region in  morph.get_regions():
    sections = list(region.sections)

    dists = [section_dist_to_dummy(s) for s in sections]
    radii = [s.d_r for s in sections]

    ax1.plot(dists, radii, 'o', label="Region: %s" % region.name)

ax1.legend()
pylab.show()

