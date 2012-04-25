#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import atexit
import sys
import os
import cStringIO
import time
import traceback
import datetime
import inspect
import signal
from scripttools.plotmanager import PlotManager




sys.path.append( '/home/michael/hw/morphforge/src/mhlibs/simulation_manager/' ) 
sys.path.append( '/home/michael/hw/morphforge/src/mhlibs/simulation_manager/simmgr/' ) 

from django.core.management import setup_environ
from simmgr import settings
setup_environ(settings)



class SimulationDBWriter(object):
    @classmethod
    def write_to_database( cls, sim_run_info):
        from simmgr.sm1.models import SimulationFile
        from simmgr.sm1.models import SimulationFileRun
        from simmgr.sm1.models import get_file_md5sum

        print 'Script: ', sim_run_info.script_name

        # We don't neeed to update this file every time:
        if sim_run_info.script_name == '/home/michael/hw/morphforge/src/bin/SimulateBundle.py':
          return 

        # Find the previous SimulationFile object:
        try:
            sf = SimulationFile.objects.get(full_filename=sim_run_info.script_name)
        except: # DoesNotExistError,e :
            print 'Creating SimulationFile obj'
            sf = SimulationFile(full_filename = sim_run_info.script_name)
            sf.save()

        # Create a simulation result object:
        simres = SimulationFileRun(
              simulation_file = sf,
              execution_date = datetime.datetime.now(),
              execution_time = sim_run_info.time_taken,
              return_code = sim_run_info.return_code,
              std_out = sim_run_info.std_out,
              std_err = sim_run_info.std_err,
              exception_type = sim_run_info.exception_details[0],
              exception_traceback = str(sim_run_info.exception_details[2]),
              simulation_md5sum = get_file_md5sum(sf.full_filename),
              library_md5sum = '00000',
              output_images =  sim_run_info.output_images )

        simres.save()
           
        # Debugging
        #print sf.simulation_file_run_set 


class SimulationRunInfo(object):
 def __init__(self, script_name ):
    self.return_code = None
    self.time_taken = None
    self.time_out = None
    self.std_out = None
    self.std_err = None
    self.exception_details = None,None

    self.script_name = script_name
    self.output_images = []



class IOStreamDistributor(object):
    def __init__(self, outputs):
        self.outputs = outputs

    def write(self,  *args, **kwargs):
        for op in self.outputs:
            op.write(*args, **kwargs)

    def flush(self):
        for op in self.outputs:
          try:
            op.flush()
          except:
            pass




class TimeoutException(Exception):
  pass


class SimulationDecorator(object):
    
    start_time = None
    time_out = None
    is_initialised = False    
    exception_details = None,None,None

    std_out = None
    std_err = None
    script_name = None




    @classmethod
    def exit_handler(cls, *args, **kwargs):

        info = SimulationRunInfo( cls.script_name)

        # Read and restore the StdOut/Err
        info.std_out = cls.std_out.getvalue() 
        sys.stdout = sys.__stdout__
        info.std_err = cls.std_err.getvalue() 
        sys.stderr = sys.__stderr__


        # Pick-up any saved images:
        info.outputimages = PlotManager.figures_saved

        # Get the return value:
        info.return_code = 0

        # Get the timing:
        info.time_taken = int( time.time() - cls.start_time )

        # Has thier been an exception?
        info.exception_details = cls.exception_details
        if info.exception_details != (None,None,None):
          print 'Exception details', info.exception_details
          info.return_code = -1

        # Write to SimulationDataBase
        SimulationDBWriter.write_to_database(info)


    @classmethod
    def top_level_exception_handler(cls, exception_type, exception, tb, *args):
        try:
            print ""
            print "TopLevel-Handler Caught Exception:"
            print "----------------------------------"
            print "".join( traceback.format_tb(tb) )
            cls.exception_details  = exception_type, exception, ''.join( traceback.format_tb(tb) ) # traceback.format_exc() 
        except Exception as e:
            print 'INTERNAL ERROR, exception raised in top level handler!'
            print e
            sys.exit(0)

    @classmethod
    def Init(cls, time_out=None):
        assert not cls.is_initialised

        if 'MF_TIMEOUT' in os.environ:
            time_out = int( os.environ['MF_TIMEOUT'] )


        # Filename of the Simulation script
        cwd = os.getcwd()
        cls.script_name = os.path.join( cwd, traceback.extract_stack()[0][0] )

        #Intercept StdOut and StdErr:
        cls.std_out = cStringIO.StringIO()         
        sys.stdout = IOStreamDistributor( [cls.std_out, sys.stdout] ) 
        cls.std_err = cStringIO.StringIO()         
        sys.stderr = IOStreamDistributor( [cls.std_err, sys.stderr] ) 

        # Set an exit handler and a top level exception-handler
        # Set a top level exception handler:
        atexit.register( cls.exit_handler )
        sys.excepthook = cls.top_level_exception_handler 


        # Set a time-out alarm
        cls.start_time = time.time()
        cls.time_out = time_out

        def timeout_sighandler(signum, frame):
          raise TimeoutException()

        if time_out:
          signal.signal(signal.SIGALRM, timeout_sighandler)
          signal.alarm(time_out)
        
