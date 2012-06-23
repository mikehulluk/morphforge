#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import numpy as np

from morphforge.core import Exists, FileIO
import subprocess
from morphforge.core import RCMgr, MockControl
from morphforge.simulation.core import Simulation, SimulationResult

from morphforge.simulation.simulationmetadatabundle.builders import MetaDataBundleBuilder

from objects import MNeuronBaseSetup
from simulationdatacontainers import MHocFile, MHocFileData, MModFileSet

import sys
from morphforge.simulation.neuron.constants import NeuronSimulationConstants
import os
from morphforge.core.mgrs.logmgr import LogMgr
import time



def _random_walk(t_steps, std_dev):
    nums = (np.random.rand(t_steps)-0.5) * std_dev
    walk = np.cumsum(nums)
    return walk


class MNeuronSimulation(Simulation):

    def __init__(self, name=None, environment=None, **kwargs):
        super(MNeuronSimulation, self).__init__(name=name, environment=environment, **kwargs)

        self.simulation_objects = [ MNeuronBaseSetup(self.simsettings, simulation=self) ]
        self.recordableNames = set()


    def run(self, do_spawn=True):
        #return
        if do_spawn:
            return self._run_spawn()
        else:
            return self._run_no_spawn()


    def _run_spawn(self):

        LogMgr.info("_run_spawn() [Pickling Sim]")
        b, resfilename = MetaDataBundleBuilder.build_std_pickler(self)
        bundlefilename, simCmd = b.write_to_file_and_get_exec_string()

        #if Exists(resfilename):
        #    os.unlink(resfilename)


        if not Exists(resfilename):

            # Setup the LD_LIBRARY PATH:
            # It may be nessesary to add the following to .mfrc
            # ld_library_path_suffix = /home/michael/hw/morphforge/src/morphforgecontrib/neuron_gsl/cpp
            ld_path_additions = RCMgr.get("Neuron","ld_library_path_suffix").split(":")
            old_ld_path = os.environ.get('LD_LIBRARY_PATH','')
            os.environ['LD_LIBRARY_PATH'] = ":".join( [old_ld_path] + ld_path_additions )

            LogMgr.info("_run_spawn() [Spawning subprocess]")
            #retCode = ExecCommandGetRetCode(simCmd)
            retCode = subprocess.call( simCmd, shell=True)
            if retCode != 1: raise ValueError("Unable to simulate %s" % self.name)
            LogMgr.info("_run_spawn() [Finished spawning subprocess]")


        # Load back the results:
        LogMgr.info("_run_spawn() [Loading results]")
        self.result = SimulationResult.load_from_file(resfilename)
        LogMgr.info("_run_spawn() [Finished loading results]")


        # We have to do this so that the simulation object
        # within the result is correct!!
        self.result.simulation = self


        return self.result




    def run_return_random_walks(self):
        from morphforge.traces import  Trace_VariableDT
        # Create the HOC and ModFiles:
        hocData = MHocFile()
        modFiles = MModFileSet()
        for o in self.simulation_objects:
            o.build_hoc(hocData)
            o.build_mod(modFiles)


        time_array = np.linspace(0, 2000, num=1000) * NeuronSimulationConstants.TimeUnit
        traces = []
        records = hocData[MHocFileData.Recordables]
        for r, hocDetails in records.iteritems():

            dataArray = _random_walk(len(time_array), 0.05 ) * r.get_unit()

            tr = Trace_VariableDT(name=r.name, comment=r.get_description(), time=time_array, data=dataArray, tags=r.get_tags() )
            traces.append(tr)

        self.result = SimulationResult(traces, self)
        return self.result


    def _run_no_spawn(self):
        from morphforge.traces import  Trace_VariableDT


        # Generate Random data:
        if MockControl.is_mock_simulation:
            return self.run_return_random_walks()













        def nrn(func, *args, **kwargs):
            f = func(*args, **kwargs)
            if f != 1.0: raise ValueError("nrn Command Failed")


        # Create the HOC and ModFiles:
        hocData = MHocFile()
        modFiles = MModFileSet()
        for o in self.simulation_objects:
            #print 'BUILDING HOC:', o
            o.build_hoc(hocData)
            #print 'BUILDING MOD:', o
            o.build_mod(modFiles)



        tModBuildStart = time.time()
        modFiles.build_all()
        print "Time for Building Mod-Files: ",  time.time() - tModBuildStart


        # Open Neuron:
        import neuron
        h = neuron.h

        # Insert the mod-files:
        for mf in modFiles:
            nrn(h.nrn_load_dll, mf.get_built_filename_full())


        # Write the HOC file:
        tSimStart = time.time()
        hocFilename = FileIO.write_to_file( str(hocData), suffix=".hoc")
        nrn(h.load_file, hocFilename )
        self.hocfilename = hocFilename

        # run the simulation
        class Event(object):
            def __init__(self):
                self.interval = 5.0
                self.fih = h.FInitializeHandler(0.01, self.callback)

            def callback(self) :
                print self, "t=", h.t , "ms"
                sys.stdout.flush()
                if h.t + self.interval  < h.tstop:
                    h.cvode.event(h.t + self.interval, self.callback)

        e = Event()
        print "Running Simulation"
        h.run()
        #nrn( h.run )
        assert h.t+1 >= h.tstop

        print "Time for Simulation: ", time.time() - tSimStart


        # Extract the values back out:
        time_array = np.array(neuron.h.__getattribute__(NeuronSimulationConstants.TimeVectorName)) * NeuronSimulationConstants.TimeUnit

        tTraceReadStart = time.time()
        traces = []
        records = hocData[MHocFileData.Recordables]
        for r, hocDetails in records.iteritems():

            dataArray = np.array( neuron.h.__getattribute__(hocDetails["recVecName"] ) ) * r.get_unit()

            tr = Trace_VariableDT(name=r.name, comment=r.get_description(), time=time_array, data=dataArray, tags=r.get_tags() )
            traces.append(tr)
        print "Time for Extracting Data: (%d records)"%(len(records)),  time.time() - tTraceReadStart



        self.result = SimulationResult(traces, self)
        self.result.hocfilename = self.hocfilename
        return self.result





    # NEW API:
    def add_cell_backend_specific(self, cell):
        self.simulation_objects.append(cell)

    def add_currentclamp_backend_specific(self, cc):
        self.simulation_objects.append(cc)

    def add_voltageclamp_backend_specific(self,vc):
        self.simulation_objects.append(vc)

    def add_synapse_backend_specific(self,synapse):
        self.simulation_objects.append(synapse)

    def add_gapjunction_backend_specific(self,gapjunction):
        self.simulation_objects.append(gapjunction)

    def add_recordable(self, recordable):
        if recordable.name in self.recordableNames:
            assert False, 'Duplicate recordable name added'
        self.recordableNames.add( recordable.name )
        self.simulation_objects.append(recordable)


