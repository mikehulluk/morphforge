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

import subprocess
import sys
import os
import time

import numpy as np

from morphforge.core import FileIO
from morphforge.core import RCMgr
from morphforge.simulation.base import Simulation, SimulationResult
from morphforge.simulation.base.simulationmetadatabundle.builders import MetaDataBundleBuilder
from morphforge.simulation.neuron.objects import NeuronSimSetupObj
from morphforge.simulation.neuron.simulationdatacontainers import MHocFile
from morphforge.simulation.neuron.simulationdatacontainers import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers import MModFileSet
from morphforge.simulation.neuron.misc import NeuronSimulationConstants

from morphforge.core.mgrs.logmgr import LogMgr
from morphforge.traces import TraceVariableDT
from morphforge.core.mockcontrol import MockControl

from morphforge.simulationanalysis.summaries_new import SimulationMRedoc



def _random_walk(t_steps, std_dev):
    nums = (np.random.rand(t_steps) - 0.5) * std_dev
    walk = np.cumsum(nums)
    return walk


class NEURONSimulation(Simulation):

    def _sim_desc_str(self):
        sname = sys.argv[0]
        return '%s: %s' % (sname, self.name.replace(' ', ''))


    def __init__(self, name=None, environment=None, **kwargs):
        super(NEURONSimulation, self).__init__(
                name=name,
                environment=environment,
                **kwargs)

        self.simulation_objects = [NeuronSimSetupObj(self.simsettings,
                                   simulation=self)]
        #self.recordable_names = {}
        self.hocfilename = None




    def get_mechanisms_in_simulation(self):

        mech_id_to_obj = {}
        for cell in self.cells:
            for mech in cell.get_biophysics().get_all_mechanisms_applied_to_cell():
                m_id = mech.get_mechanism_id()
                if not m_id in mech_id_to_obj:
                    mech_id_to_obj[m_id] = []
                mech_id_to_obj[m_id].append(mech)

        for mech_id in mech_id_to_obj:
            mechobjs = mech_id_to_obj[mech_id]
            mechobj0 = mechobjs[0]
            for m in mechobjs:
                assert m is mechobj0, 'Different objects found for same id: %s' % (mech_id)
        return [ values[0] for values in mech_id_to_obj.values() ]


    def run(self, do_spawn=True):

        # Lets do some sanity checking on the mechanisms and id's:
        self.get_mechanisms_in_simulation()


        if do_spawn:
            return self._run_spawn()
        else:
            return self._run_no_spawn()

    def _run_spawn(self):

        LogMgr.info('_run_spawn() [Pickling Sim]')
        (bundle, resfilename) = MetaDataBundleBuilder.build_std_pickler(self)
        (_bundlefname, sim_cmd) = bundle.write_to_file_and_get_exec_string()

        # if Exists(resfilename):
        #    os.unlink(resfilename)

        if not os.path.exists(resfilename):

            # Setup the LD_LIBRARY PATH:
            # It may be nessesary to add the following to .mfrc
            # ld_library_path_suffix = /home/michael/hw/morphforge/src/morphforgecontrib/neuron_gsl/cpp
            ld_path_additions = RCMgr.get('Neuron', 'ld_library_path_suffix').split(':')
            old_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
            os.environ['LD_LIBRARY_PATH'] = ':'.join([old_ld_path] + ld_path_additions)

            LogMgr.info('_run_spawn() [Spawning subprocess]')
            ret_code = subprocess.call(sim_cmd, shell=True)
            if ret_code != 1:
                raise ValueError('Unable to simulate %s' % self.name)
            LogMgr.info('_run_spawn() [Finished spawning subprocess]')

        # Load back the results:
        LogMgr.info('_run_spawn() [Loading results]')
        self.result = SimulationResult.load_from_file(resfilename)
        LogMgr.info('_run_spawn() [Finished loading results]')

        # We have to do this so that the simulation object
        # within the result is correct!!
        self.result.simulation = self


        # Save the simulation summary:
        #import sys
        #sname = sys.argv[0]


        do_summary = False
        if do_summary:
            fname = '~/Desktop/pdfs/%s.pdf' % (self._sim_desc_str().replace(' ', ''))
            summary = SimulationMRedoc.build(self)
            summary.to_pdf(fname)


        return self.result

    def run_return_random_walks(self):
        # Create the HOC and ModFiles:
        hoc_data = MHocFile()
        mod_files = MModFileSet()
        for sim_obj in self.simulation_objects:
            sim_obj.build_hoc(hoc_data)
            sim_obj.build_mod(mod_files)


        time_array = np.linspace(0, 2000, num=1000) * NeuronSimulationConstants.TimeUnit
        traces = []
        records = hoc_data[MHocFileData.Recordables]
        for rec in records.keys():

            data_array = _random_walk(len(time_array), 0.05) * rec.get_unit()

            tr = TraceVariableDT(name=rec.name,
                                 comment=rec.get_description(),
                                 time=time_array, data=data_array,
                                 tags=rec.get_tags())
            traces.append(tr)

        self.result = SimulationResult(traces, self)
        return self.result

    def _run_no_spawn(self):

        # Generate Random data:
        if False or MockControl.is_mock_simulation:
            return self.run_return_random_walks()

        def nrn(func, *args, **kwargs):
            return_value = func(*args, **kwargs)
            if return_value != 1.0:
                raise ValueError('nrn Command Failed')

        # Create the HOC and ModFiles:
        hoc_data = MHocFile()
        mod_files = MModFileSet()
        for sim_obj in self.simulation_objects:
            # print 'BUILDING HOC:', sim_obj
            sim_obj.build_hoc(hoc_data)
            # print 'BUILDING MOD:', sim_obj
            sim_obj.build_mod(mod_files)

        t_mod_build_start = time.time()
        mod_files.build_all()
        time_taken = time.time() - t_mod_build_start
        print 'Time for Building Mod-Files: ', time_taken

        # Open Neuron:
        import neuron

        # Insert the mod-files:
        for modfile in mod_files:
            nrn(neuron.h.nrn_load_dll, modfile.get_built_filename_full())

        # Write the HOC file:
        t_sim_start = time.time()
        hoc_filename = FileIO.write_to_file(
                        str(hoc_data), 
                        suffix='.hoc')

        nrn(neuron.h.load_file, hoc_filename)
        self.hocfilename = hoc_filename

        #tstop = self.simsettings['tstop']
        # run the simulation
        class Event(object):

            def __init__(self):
                self.interval = 5.0
                self.fih = neuron.h.FInitializeHandler(0.01, self.callback)

            def callback(self):
                sys.stdout.write('Simulating: t=%.0f/%.0fms \r' % (neuron.h.t, float(neuron.h.tstop)))
                sys.stdout.flush()
                if neuron.h.t + self.interval < neuron.h.tstop:
                    neuron.h.cvode.event(neuron.h.t + self.interval, self.callback)

        Event()
        print 'Running Simulation'
        neuron.h.run()
        assert neuron.h.t + 1 >= neuron.h.tstop

        print 'Time for Simulation: ', time.time() - t_sim_start

        # Extract the values back out:
        time_array = np.array(neuron.h.__getattribute__(NeuronSimulationConstants.TimeVectorName)) * NeuronSimulationConstants.TimeUnit

        t_trace_read_start = time.time()
        traces = []
        records = hoc_data[MHocFileData.Recordables]
        for (record_obj, hoc_details) in records.iteritems():

            data_array = np.array(neuron.h.__getattribute__(hoc_details["recVecName"])) * record_obj.get_unit()

            tr = TraceVariableDT(name=record_obj.name,
                                 comment=record_obj.get_description(),
                                 time=time_array, data=data_array,
                                 tags=record_obj.get_tags())
            traces.append(tr)
        print 'Time for Extracting Data: (%d records)' % len(records), \
            time.time() - t_trace_read_start

        self.result = SimulationResult(traces, self)
        return self.result

    # NEW API:
    def add_cell_backend_specific(self, cell):
        self.simulation_objects.append(cell)

    def add_currentclamp_backend_specific(self, cc):
        self.simulation_objects.append(cc)

    def add_voltageclamp_backend_specific(self, vc):
        self.simulation_objects.append(vc)

    def add_synapse_backend_specific(self, synapse):
        self.simulation_objects.append(synapse)

    def add_gapjunction_backend_specific(self, gapjunction):
        self.simulation_objects.append(gapjunction)

    def add_recordable_backend_specific(self, recordable):
        self.simulation_objects.append(recordable)

    #def add_recordable(self, recordable):
    #    if recordable.name in self.recordable_names:
    #        assert False, 'Duplicate recordable name added'
    #    self.recordable_names[recordable.name] = recordable
    #    self.simulation_objects.append(recordable)


