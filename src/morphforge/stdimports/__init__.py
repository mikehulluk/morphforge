s#!/usr/bin/python
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

# pylint: disable=W0401
# pylint: disable=W0611
# (don't complain about wildcard imports)


import os
from decimal import Decimal



try:
    import pylab
    import numpy as np
except ImportError:
    print 'Problem importing Numpy or Matplotlib'


import neurounits




# Units:
import morphforge.units as units
from morphforge.units import qty
from morphforge.units import qty




from mhlibs.quantities_plot import *

# CORE
from morphforge.core import *

from morphforge.traces import *
from morphforge.traces.eventset import EventSet, Event

from morphforge.simulationanalysis.tagviewer import TagViewer
from morphforge.simulationanalysis.tagviewer import TagPlot
from morphforge.simulationanalysis.tagviewer import TagPlot as PlotSpec
from morphforge.simulationanalysis.tagviewer import DefaultTagPlots
from morphforge.simulationanalysis.tagviewer import DefaultTagPlots as DefaultPlotSpecs
from morphforge.simulationanalysis.tagviewer.linkage import StandardLinkages
from morphforge.simulationanalysis.tagviewer.linkage import LinkageRuleTagRegex
from morphforge.simulationanalysis.tagviewer.linkage import LinkageRuleTag
from morphforge.simulationanalysis.tagviewer.plotspecs import YAxisConfig

#
from morphforge.constants import *

# MORPHOLOGY:
from morphforge.morphology import *
from morphforge.morphology.core import *
from morphforge.morphology.builders import *
from morphforge.morphology.visitor import *
from morphforge.morphology.ui import *
from morphforge.morphology.util.morphlocator import MorphLocator

# SIMULATION
from morphforge.simulation.base import *
from morphforge.simulation.neuron import *
from morphforge.simulation.base.util.celllocator import CellLocator

from morphforge.simulation.base.synaptictriggers import SynapticTriggerAtTimes
from morphforge.simulation.base.synaptictriggers import SynapticTriggerByVoltageThreshold



from morphforge.componentlibraries import *
from morphforge.componentlibraries.psm_template_library import PostSynapticTemplateLibrary
from morphforge.componentlibraries.channellibrary import cached_functor

# Import to ensure that they are registered with the plugin-system:
import morphforge.simulation.neuron.objects.obj_cclamp
import morphforge.simulation.neuron.objects.obj_vclamp

from morphforge.morphology.conventions import SWCRegionCodes




from morphforge.morphology.core.tree import MorphPath
from morphforge.simulation.base.segmentation.cellsegmenter import CellSegmenter_MaxLengthByID



from morphforge.management import PluginMgr
from morphforge.simulationanalysis.summaries_new import SimulationMRedoc





class MembraneMechanismSummariser(object):
    @classmethod
    def create_pdf(cls, *args, **kwargs):
        pass



from morphforge.simulationanalysis.summaries_new import SummariserLibrary
from morphforge.simulationanalysis.summaries_new import SummariserOptions



try:
    from mreorg import PM
except ImportError:
    pass

















# Some basic caching.
# Note that this code looks at every lin of pytohn code that has been run in the
# funciton and makes sure that it hasn't changes.
# WHAT IS MISSING IS CODE TO ENSURE THAT DURING LOADUP - THE SAME HAPPENS.
# WE CAN PROBABLY DO THIS BY INSERTING ANOTHER CALL VERY EARLY ON DURING STARTUP
# AND ALSO CACHING WHAT IS CALLED IN THAT!
# WITH THE CURRENT CACHING, IF INITITAILISATION CODE CHANHGES A Variable that it later
# read, we don't pick this up!


import trace,hashlib, sys, os
import cPickle, inspect



class HashManager(object):
    _file_hashes = {}
    @classmethod
    def get_filename_hash(cls, filename):
        if not filename in cls._file_hashes:
            with open(filename) as fobj:
                hashobj = hashlib.new('sha1')
                hashobj.update(fobj.read())
            cls._file_hashes[filename] = str(hashobj.hexdigest())
        return cls._file_hashes[filename]

class _CachedFileAccessData(object):
    def __init__(self, filename, linenumbers):
        self.filename = filename
        self.linenumbers = linenumbers
        self._cachedhashfile = HashManager.get_filename_hash(filename)
        self._cachedhashlines = self.current_line_hash()


    def current_line_hash(self):

        lines = self.get_file_lines()
        if lines is not None:
            hashobj = hashlib.new('sha1')
            hashobj.update('\n'.join(lines ))
            return hashobj.hexdigest()
        else:
            return None


    def get_file_lines(self):
        with open(self.filename) as fobj:
            lines = fobj.readlines()

        res = []
        n_lines = len(lines)
        for linenumber in self.linenumbers:
            if not linenumber < n_lines:
                return None
            res.append(lines[linenumber])
        return res



    def is_clean(self):
        if self._cachedhashfile == HashManager.get_filename_hash(self.filename):
            return True
        if self._cachedhashlines is not None and \
           self._cachedhashlines == self.current_line_hash():
            return True



        return False

    def __str__(self,):
        return '<CachedFileObject: (is_clean:%s) %s [%s->%s]>' % (self.is_clean(), self.filename, self._cachedhashfile, HashManager.get_filename_hash(self.filename))

def load_cache(cachefilename):
    if not os.path.exists(cachefilename):
        return None, None
    with open(cachefilename) as fobj:
        (return_value, cache_data) = cPickle.load(fobj)
        return (return_value, cache_data)

def save_cache(cachefilename, return_value, cache_data):
    LocMgr.ensure_dir_exists(os.path.dirname(cachefilename))
    with open(cachefilename, 'w') as fobj:
        res = (return_value, cache_data)
        cPickle.dump( res, fobj)

def _run_and_cache(func, args, kwargs):
    trace_obj = trace.Trace( count=1, trace=0, countfuncs=0,
            ignoredirs=[sys.prefix, sys.exec_prefix])

    output = trace_obj.runfunc(func, *args, **kwargs)

    _accessed_functions = {}
    for (filename, linenumber) in sorted(trace_obj.results().counts):
        if filename .startswith('/usr'):
            continue
        if filename.startswith("build/bdist.linux-x86_64/egg/"):
            continue

        if not filename in _accessed_functions:
            _accessed_functions[filename] = []
        _accessed_functions[filename].append(linenumber)

    cache_data = []
    for filename, linenumbers in _accessed_functions.iteritems():
        if filename == '<string>':
            assert False
        else:
            cd = _CachedFileAccessData(filename=filename, linenumbers=linenumbers)
            cache_data.append(cd)
    return (output, cache_data)


def is_cache_clean(cache):
    print 'Is the cache clean?'
    if cache is None:
        return False

    for cachefile in cache:
        if not cachefile.is_clean():
            print 'No! ( Out of date: %s )' % cachefile
            return False
    print 'Yes (No changes detected in %d files)' % len(cache) 
    return True


def get_arg_string_hash(args, kwargs):
    arg_strs = [cPickle.dumps(arg) for arg in args]
    kwargs_strs = ['%s=%s' % (str(key), cPickle.dumps(value)) for (key,value) in sorted( kwargs.iteritems()) ]

    res = ','.join( arg_strs + kwargs_strs)
    hashobj = hashlib.new('sha1')
    hashobj.update(res)
    return hashobj.hexdigest()

def run_with_cache(func, args=None, kwargs=None, cachefilenamebase=None):
    if cachefilenamebase is None:
        if RCMgr.has('Locations', 'simulation_cache'):
            cachefilenamebase = RCMgr.get( 'Locations', 'simulation_cache' )
        else:
            print 'Unable to find suitable cache-directory. Either pass it as an option to this function, or add to the morphforge config file in Locations:simulation_cache'
            print
            assert False

        #cachefilenamebase = '/mnt/sdb5/home/michael/mftmp/_cache/cache'
        #cachefilenamebase = '/local/scratch/mh735/tmp/mf_cache/'

    # Hash up the arguments:
    if not args:
        args=tuple()
    if not kwargs:
        kwargs={}
    arg_hash = get_arg_string_hash(args, kwargs)
    script_filename = inspect.stack()[-1][1]
    script_filename_clean = script_filename.replace('/','__').replace(' ','__').replace('.', '_')
    cachefilename = cachefilenamebase + '_' + script_filename_clean + '_' + arg_hash + '.pickle'
    print(cachefilename)
    print("\n")

    return_value, cache = load_cache(cachefilename=cachefilename)
    if not is_cache_clean(cache):
        return_value, cache = _run_and_cache(func, args=args, kwargs=kwargs)
        save_cache(cachefilename, return_value, cache)
    return return_value














