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
# AJAX:
from django.utils import simplejson
#from dajaxice.core import dajaxice_functions
from dajaxice.decorators import dajaxice_register
#import random
from models import SimulationFile, SimulationQueueEntry, SimRunStatus,SimulationQueueEntryState

import datetime

@dajaxice_register
def setSimulationFileForResubmit(request, simulation_file_id):
    print 'Setting for resubmit',simulation_file_id
    try:
        sim_file = SimulationFile.objects.get(id = simulation_file_id)
    except:
        return simplejson.dumps({})
    

    # Existing simulation object
    if sim_file.simulationqueueentry_set.count() != 0:
        return simplejson.dumps({})
    else:
        qe = SimulationQueueEntry( simulation_file = sim_file )
        qe.save()
        return simplejson.dumps({})
        

@dajaxice_register
def setSimulationFileForResubmitIfFailure(request, simulation_file_id):
    print 'Setting for resubmit',simulation_file_id
    
    try:
        sim_file = SimulationFile.objects.get(id = simulation_file_id)
    except:
        return simplejson.dumps({})


    if sim_file.get_status() == SimRunStatus.Sucess:
        return simplejson.dumps({})

    # Existing simulation object
    if sim_file.simulationqueueentry_set.count() != 0:
        return simplejson.dumps({})
    else:
        qe = SimulationQueueEntry( simulation_file = sim_file )
        qe.save()
        return simplejson.dumps({})
        



@dajaxice_register
def toggleSimulationFileForResubmit(request, simulation_file_id):
    #print 'Toggling',simulation_file_id
    #print
    try:
        sim_file = SimulationFile.objects.get(id = simulation_file_id)
    except:
        return simplejson.dumps({})

    # Existing simulation object
    if sim_file.simulationqueueentry_set.count() != 0:
        sim_file.simulationqueueentry_set.all().delete()
        return simplejson.dumps({})
    else:
        qe = SimulationQueueEntry( simulation_file = sim_file )
        qe.save()
        return simplejson.dumps({})


@dajaxice_register
def refreshsimlist(request):

    states = {}
    for simfile in SimulationFile.objects.all():
        states[simfile.id] = simfile.get_status()
    return simplejson.dumps({'sim_file_states':states})


@dajaxice_register
def updateSimGui(request, simulation_file_id):
    sim_file = SimulationFile.objects.get(id = simulation_file_id)
    exec_date = ""
    if sim_file.get_latest_run():
        exec_date = sim_file.get_latest_run().execution_data_string()

    return simplejson.dumps( 

                {'sim_id':simulation_file_id,
                 'state':sim_file.get_status(),
                 'is_queued':sim_file.is_queued(),
                 'latest_exec_id':sim_file.get_latest_run().id if sim_file.get_latest_run() else "",
                 'latest_exec_date': exec_date,
                } )



@dajaxice_register
def clearSimQueue(request, ):
    SimulationQueueEntry.objects.all().filter( status = SimulationQueueEntryState.Waiting ).delete() 
    return simplejson.dumps({})

@dajaxice_register
def deleteSimulationFile(request, simulation_file_id ):
    print "deleting sim"

    try:
        sim_file = SimulationFile.objects.get(id = simulation_file_id)
        sim_file.delete()
    except:
        pass
    print 'deleteing OK'
    return simplejson.dumps({})
