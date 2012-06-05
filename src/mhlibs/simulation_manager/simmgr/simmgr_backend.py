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
import sys
# Setup link to django models:
sys.path.append( '/home/michael/hw/morphforge/src/mhlibs/simulation_manager/' ) 
from django.core.management import setup_environ
from simmgr import settings
setup_environ(settings)

import time
import os
import datetime
import subprocess

from simmgr.sm1.models import SimulationQueueEntry
from simmgr.sm1.models import SimulationQueueEntryState



#Setup the environment,
os.environ['MF_BATCH']='TRUE'
os.environ['MF_TIMEOUT'] = '180'
os.environ['MF_TEST_COVERAGE'] = ''


def simulate( simulation_queue_entry):
  filename = simulation_queue_entry.simulation_file.full_filename
  print ' - Simulating: ', filename
  dname, fname = os.path.split(filename)

  # Update the database to reflect 
  print '   - Updating database'
  simulation_queue_entry.status = SimulationQueueEntryState.Executing
  simulation_queue_entry.simulation_start_time = datetime.datetime.now()
  simulation_queue_entry.save(force_update=True)


  # Simulate:
  print '   - Changing Directory to', dname
  os.chdir(dname)
  try:
    subprocess.check_call(["python", fname])
    print '   - Finished Simulating [Exit OK]'
  except subprocess.CalledProcessError as e:
    print '   - Finished Simulating [Non-zero exitcode]'
    if not simulation_queue_entry.simulation_file.get_latest_run():
      print 'Simulation not decorated! Unable to set return code'
    else:
      simulation_queue_entry.simulation_file.get_latest_run().returncode = e.returncode
      simulation_queue_entry.simulation_file.get_latest_run().save(force_update=True)

    
  # Remove the simulation_queue_entry:
  simulation_queue_entry.delete()




while True:
  time.sleep(1)
  print 'Checking for Queued Simulations'

  queued_objects = SimulationQueueEntry.objects.filter(status=SimulationQueueEntryState.Waiting).order_by('submit_time')
  #queued_objects = SimulationQueueEntry.objects.order_by('submit_time')

  # Nothing to simulate:
  if not queued_objects:
    print ' - No Simulations found'
    continue

  # Simulate the first object:
  simulate( queued_objects[0] )





