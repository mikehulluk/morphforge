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

import time
t_start = time.time()

import sys
from morphforge.core import LogMgr, mfrandom
from morphforge.simulation.base.simulationmetadatabundle import SimMetaDataBundle

import traceback

# Lets not buffer any output:
class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()
#sys.stdout = flushfile(sys.stdout)
#sys.stderr = flushfile(sys.stderr)


class TracePrints(object):
  def __init__(self):    
    self.stdout = sys.stdout
  def write(self, s):
    self.stdout.write("Writing %r\n" % s)
    traceback.print_stack(file=self.stdout)

#sys.stdout = TracePrints()



def main():

    bundleFilename = sys.argv[1]
    print "Loading Bundle from ", bundleFilename
    bundle = SimMetaDataBundle.load_from_file(bundleFilename)

    # Load the random number seed
    if bundle.random_seed is not None:
        mfrandom.MFRandom.seed(bundle.random_seed)


    result = bundle.get_simulation().run(do_spawn=False)
    result.set_simulation_time(t_start, time.time())

    #LogMgr.info("Simulation Ran OK. Post Processing:")

    bundle.do_postprocessing_actions()
    #LogMgr.info("Bundle Completed OK")





try:
    t_start = time.time()
    main()
    tEnd = time.time()
    print "Simulation Time Elapsed: ", tEnd - t_start
except:
    import traceback
    traceback.print_exc()
    print "Simulation Failled"
    sys.exit(0)



print "Suceeded"
sys.exit(1)
