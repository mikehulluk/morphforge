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
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
#from django.views.generic.simple import redirect_to
from django.http import HttpResponseRedirect
from models import SimulationFile
from models import SimRunStatus
from models import SimulationFileRun
from models import SimulationQueueEntry
from models import SimulationQueueEntryState
from models import PotentialSimulationFile
from models import PotentialSimulationDirectory
from django.template import RequestContext


import os
import re
from urlparse import urlsplit 



# Index page:
def index(request):
    c = {'simulation_files': SimulationFile.objects.all() }
    csrfContext = RequestContext(request, c)
    return render_to_response('simulation_overview.html',csrfContext )



def view_simulation_output_summaries(request):
    sims = SimulationFile.objects.all()
    sim_and_dir = [ (s,os.path.dirname(s.full_filename)) for s in sims]
    sim_and_dir.sort()

    sim_dirs = sorted( set([ s[1] for s in sim_and_dir] ) )
    
    print sim_dirs

    common_prefix = os.path.commonprefix(sim_dirs)
    print common_prefix

    op = []
    for sd in sim_dirs:
        sd_short = '.../'+sd.replace(common_prefix,"")
        sims_o = sorted( [s[0] for s in sim_and_dir if s[1]==sd ], key= lambda s:s.full_filename )
        op.append( (sd_short, sims_o) ) 

    c = {'simulation_files': [
            ('jlkd/',sims)
            ]
            }

    c = {'simulation_files': op }
    csrfContext = RequestContext(request, c)
    return render_to_response('simulation_output_summaries.html',csrfContext )





def simulationfilerun_details(request, id):
    simrun =  SimulationFileRun.objects.get(id=id)
    #images = simrun.output_images.all()
    #for i in images:
    #    i.hash_thumbnailname_short()
    r = RequestContext(request, {'simulationrun':simrun,})#'images':images} )
    return render_to_response('simulation_run_details.html',r)





def simulationfile_details(request, id):
    sim =  SimulationFile.objects.get(id=id)
    return render_to_response('simulation_file_details.html',{'simulationfile':sim})

def viewpotentialsimulationfiles(request,):
    potential_files = PotentialSimulationFile.objects.all().order_by('full_filename')
    potential_directories = PotentialSimulationDirectory.objects.all().order_by('directory_name')
    c = {'potentialsimulationfiles': potential_files,'potential_directories':potential_directories} 
    csrfContext = RequestContext(request, c)
    return render_to_response('potential_simulation_files.html',csrfContext)




def doaddpotentialsimulationlocation(request):
    if request.method!='POST':
      return HttpResponseRedirect('/viewpotentialsimulationfiles')

    PotentialSimulationDirectory.addLocation(location=request.POST['location'])
    return HttpResponseRedirect('/viewpotentialsimulationfiles')


def doupdatepotentialsimulationfiles(request,):

    for potential_location in PotentialSimulationDirectory.objects.all():
      PotentialSimulationFile.update_all_db( potential_location.directory_name) 
    return HttpResponseRedirect('/viewpotentialsimulationfiles')

def dopotentialtoactualsimulationfiles( request):
  if not request.method == 'POST':
    return HttpResponseRedirect('/viewpotentialsimulationfiles')


  # Find all keys matching potentialsimid_XX, and get the XX's
  r = re.compile(r"""potentialsimid_(?P<id>\d+)""", re.VERBOSE)
  pot_sim_id_matches = [ r.match(k) for k in request.POST ] 
  pot_sim_ids = [ int(m.groupdict()['id'] ) for m in pot_sim_id_matches if m] 
  

  for pot_sim_id in pot_sim_ids:
    pot_sim = PotentialSimulationFile.objects.get(id=pot_sim_id)

    sim = SimulationFile( full_filename = pot_sim.full_filename )
    
    sim.save()
    pot_sim.delete()

  
  return HttpResponseRedirect('/')



def viewsimulationqueue(request):
    c = {'simulation_queue_executing': SimulationQueueEntry.objects.filter(status=SimulationQueueEntryState.Executing),
         'simulation_queue': SimulationQueueEntry.objects.filter(status=SimulationQueueEntryState.Waiting), 
         'latest_runs': SimulationFileRun.objects.order_by('-execution_date')[0:10] }

    csrfContext = RequestContext(request, c)
    return render_to_response('view_simulation_queue.html',csrfContext)

def view_simulation_failures(request):
    fileObjs =  SimulationFile.objects.all()

    c = {
        'failed_simulations': [fo for fo in fileObjs if fo.get_status() == SimRunStatus.UnhandledException ],
        'timeout_simulations': [fo for fo in fileObjs if fo.get_status() == SimRunStatus.TimeOut ],
        'nonzero_exitcode_simulations': [fo for fo in fileObjs if fo.get_status() == SimRunStatus.NonZeroExitCode],
        'changed_simulations': [fo for fo in fileObjs if fo.get_status() == SimRunStatus.FileChanged ],
        'notrun_simulations': [fo for fo in fileObjs if fo.get_status() == SimRunStatus.NeverBeenRun ],
        } 

      
    csrfContext = RequestContext(request, c)
    return render_to_response('view_simulation_failures.html',csrfContext)





def doremovesimulationsfromqueue(request):
  return HttpResponseRedirect('/viewsimulationqueue')

def doqueuesimulations(request):
  if not request.method == 'POST':
    return HttpResponseRedirect('/viewsimulationqueue')

  print 'Queuing Simulations:'
  print request.POST
  r = re.compile(r"""simid_(?P<id>\d+)""", re.VERBOSE)
  sim_id_matches = [ r.match(k) for k in request.POST ] 
  sim_ids = [ int(m.groupdict()['id'] ) for m in sim_id_matches if m] 
  

  for sim_id in sim_ids:
    sim = SimulationFile.objects.get(id=sim_id)

    qe = SimulationQueueEntry( simulation_file = sim )
    qe.save()
    #Avoid Duplication

  return HttpResponseRedirect('/viewsimulationqueue')


  
def doeditsimulationfile(request, simulationfile_id):

  #Open up the file in an editor:
  sim = SimulationFile.objects.get(id=simulationfile_id)

  cwd = os.getcwd()
  os.chdir( os.path.split(sim.full_filename)[0])
  os.system('xterm &')
  os.chdir(cwd)
  os.system('gvim "%s"'%sim.full_filename)


  # Return to the previous page:
  referer = request.META.get('HTTP_REFERER', None) 
  if referer is None: 
    return HttpResponseRedirect('/')       

  try: 
    redirect_to = urlsplit(referer, 'http', False)[2] 
    return HttpResponseRedirect(redirect_to)
  except IndexError: 
    return HttpResponseRedirect('/')       



def view_mhactions(self):
    return render_to_response('view_mh_actions.html',csrfContext)


def mh_adddefault_locations(self):
    locations = [
          #'/home/michael/hw/hw-results/src/',
          '/home/michael/hw/morphforge/src/morphforge/examples/',
          '/home/michael/hw/signalanalysis/reports/',
        
                ]
    for loc in locations:
      PotentialSimulationDirectory.addLocation(location=loc)
    return HttpResponseRedirect('/')       








