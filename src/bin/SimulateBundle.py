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

# Import the AGG backend, since it loads fast:
import matplotlib
matplotlib.use('Agg')



import time
t_start = time.time()

import sys, os
from morphforge.core import mfrandom
#from morphforge.core import LogMgr, mfrandom
from morphforge.simulation.base.simulationmetadatabundle import SimMetaDataBundle

import traceback
import time
from morphforge.core.misc import  benchmark#, TracePrints

## Lets not buffer any output:
#class flushfile(file):
#    def __init__(self, f):
#        self.f = f
#    def write(self, x):
#        self.f.write(x)
#        self.f.flush()
##sys.stdout = flushfile(sys.stdout)
##sys.stderr = flushfile(sys.stderr)
#
#class benchmark(object):
#    def __init__(self,name):
#        self.name = name
#    def __enter__(self):
#        self.start = time.time()
#    def __exit__(self,ty,val,tb):
#        end = time.time()
#        print("%s : %0.3f seconds" % (self.name, end-self.start))
#        return False
#
#class TracePrints(object):
#  def __init__(self):    
#    self.stdout = sys.stdout
#  def write(self, s):
#    self.stdout.write("Writing %r\n" % s)
#    traceback.print_stack(file=self.stdout)
#
##sys.stdout = TracePrints()


def main():

    bundleFilename = sys.argv[1]
    with benchmark('Loading Bundle from: %s (%dk)'%(bundleFilename, os.path.getsize(bundleFilename)/1000 ) ):
        bundle = SimMetaDataBundle.load_from_file(bundleFilename)

    # Load the random number seed
    if bundle.random_seed is not None:
        mfrandom.MFRandom.seed(bundle.random_seed)


    with benchmark('Running simulation'):
        result = bundle.get_simulation().run(do_spawn=False)
        result.set_simulation_time(t_start, time.time())

    #LogMgr.info("Simulation Ran OK. Post Processing:")

    with benchmark('Post-processing'):
        bundle.do_postprocessing_actions()

    #LogMgr.info("Bundle Completed OK")





try:
    with benchmark('Entire load-run-save time'):
        main()
except:
    #import traceback
    traceback.print_exc()
    print "Simulation Failled"
    sys.exit(0)



print "Suceeded"
sys.exit(1)
