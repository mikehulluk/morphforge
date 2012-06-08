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
from django.db import models
import os
import re
import hashlib
import datetime

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def get_file_md5sum(filename):
    m = hashlib.md5()
    with  open(filename) as f:
        m.update( f.read() )
    return m.hexdigest()



class PotentialSimulationDirectory(models.Model):
  directory_name = models.CharField(max_length=1000)

  def does_exist(self):
    return os.path.exists( self.directory_name)

  @classmethod
  def addLocation(cls, location):
    if PotentialSimulationDirectory.objects.filter(directory_name = location).count() !=0:
      return 

    # Create and save
    p = PotentialSimulationDirectory(directory_name=location)
    p.save()



class PotentialSimulationFileStatus(object):
  Tracked='Tracked'
  Unknown='Unknown'
  NotTracked='Nottracked'
  

class PotentialSimulationFile(models.Model):
  full_filename = models.CharField(max_length=1000)
  status = models.CharField( max_length=1000)


  @classmethod 
  def create(self, filename):
    try:
      SimulationFile.objects.get(full_filename=filename)
      print 'Already a simulation file'
      return  
    except:
      pass
    
    try: 
        PotentialSimulationFile.objects.get( full_filename = filename)
        print 'Already a potential simulation file'
        return None
    except:
      pass

    # Create a new potential simulation file object:
    p = PotentialSimulationFile( full_filename = filename, status = PotentialSimulationFileStatus.Unknown )
    p.save()

  @classmethod
  def update_all_db(cls, directory):
    excludes = ('py.py','__init__.py' )

    def accept_file( filename ):
      if not filename.endswith('.py'):
        return False
      if filename.startswith("__"):
        return False

      dirname, fname = os.path.split(filename)
      if fname in excludes:
        return False
      return True
    
    def handlefile(filename):
      print 'Checking: ', filename
      p = PotentialSimulationFile.create(filename) 


    print 'Updating potential simulation files', directory
    for (dirpath, dirnames, filenames) in os.walk( directory ):
      for filename in filenames:
        if accept_file(filename): 
          handlefile( os.path.join( dirpath, filename ) )






#ds = re.compile(r"""^ \s* (?P<quotes> \"{3} | \"{1} | ' | ''' ) (?P<ds>.*?) (?P=quotes) """, re.VERBOSE | re.MULTILINE| re.DOTALL)
#def extract_docstring_from_file(f):
#    fd = open(f)
#    m = ds.match( fd.read() )
#    fd.close()
#    if not m: 
#        return None
#    return m.groupdict().get('ds',None)

def extract_docstring_from_file(f):
    import tokenize, token
    f=open(f)
    for tok, text, (srow, scol), (erow,ecol), l in tokenize.generate_tokens(f.readline):
        if tok in [tokenize.COMMENT, tokenize.NL]:
            continue
        elif tok in [ tokenize.NAME,tokenize.ENDMARKER] :
            return None
        elif tok == tokenize.STRING:
            t = text.strip()
            if t.startswith('"""'):
                t = t[3:]
            if t.endswith('"""'):
                t = t[:-3]
            return t.strip()
        else:
            print 'tok',tok, token.tok_name[tok]
            assert False
    return None



class SimRunStatus(object):
    Sucess = 'Sucess'
    UnhandledException = 'UnhandledException'
    TimeOut = 'Timeout'
    NonZeroExitCode = 'NonZeroExitCode'
    
    FileChanged = 'FileChanged'
    NeverBeenRun = 'NeverBeenRun'



class SimulationFile(models.Model):

  class Meta():
    ordering = ['full_filename']


  full_filename = models.CharField(max_length=1000)

  def doesFileExist(self):
      return os.path.exists(self.full_filename)


  def get_html_code(self):
    code = 'print "Hello World"'
    with open(self.full_filename) as f:
      code = f.read()
    html = highlight(code, PythonLexer(), HtmlFormatter())
    return html




  def get_current_checksum(self):
    return get_file_md5sum(self.full_filename)

  def get_short_filename(self):
    fn = os.path.split(self.full_filename)[1]
    return fn
  
  def get_description(self):
    return extract_docstring_from_file( self.full_filename)


  def get_runs(self):
    return SimulationFileRun.objects.filter(simulation_file=self.id).order_by('-execution_date')
  
  def get_latest_run(self):
    runs = self.get_runs()
    if not runs:
        return None
    else:
        return runs[0]

  def get_status(self):
    last_run = self.get_latest_run()
    if not last_run:
      return SimRunStatus.NeverBeenRun
    else:
      return last_run.get_status()

  def get_last_executiontime(self):
    last_run = self.get_latest_run()
    if not last_run:
      return 'Unknown'
    else:
      return last_run.execution_time

  def is_queued(self):
    return self.simulationqueueentry_set.count() != 0

  def getCSSQueueState(self):
      p = self.is_queued()
      LUT = { True:'SimulationQueued',False:'SimulationNotQueued'}
      return LUT[p]




class SimulationFileRun(models.Model):
  simulation_file = models.ForeignKey(SimulationFile)
  execution_date = models.DateTimeField('execution date')
  return_code = models.IntegerField()
  std_out = models.CharField(max_length=10000000)
  std_err = models.CharField(max_length=10000000)
  #output_images = models.CharField(max_length=50000)
  exception_type = models.CharField(max_length=10000,null=True, blank=False)
  exception_traceback = models.CharField(max_length=10000,null=True, blank=False)

  simulation_md5sum = models.CharField(max_length=200)
  library_md5sum = models.CharField(max_length=200)
  execution_time = models.IntegerField(null=True)

  def execution_data_string(self):
        import datetime
        exec_date = str(self.execution_date)
        print exec_date
        #2012-01-02 14:28:29.129076
        d = datetime.datetime.strptime(exec_date,'%Y-%m-%d %H:%M:%S.%f')
        print d
        s = d.strftime('%Y-%m-%d %H:%M')
        return s

  def is_script_uptodate(self):
    res = str(self.simulation_md5sum) == str(self.simulation_file.get_current_checksum())
    return res

  def get_status(self):
    
        if self.simulation_md5sum != self.simulation_file.get_current_checksum():
            return SimRunStatus.FileChanged
        if self.execution_time is None:
            return SimRunStatus.TimeOut
        if self.exception_type:
            if 'TimeoutException' in self.exception_type:
                return SimRunStatus.TimeOut

            return SimRunStatus.UnhandledException
        if self.return_code != 0:
            return SimRunStatus.NonZeroExitCode
        return SimRunStatus.Sucess

class SimulationFileRunOutputImage(models.Model):
    original_name = models.CharField(max_length=10000)
    hash_name = models.CharField(max_length=10000)
    hash_thumbnailname = models.CharField(max_length=10000)
    simulation = models.ForeignKey(SimulationFileRun, related_name='output_images')

    def hash_name_short(self):
        return self.hash_name.split("/")[-1]
    def hash_thumbnailname_short(self):
        return self.hash_thumbnailname.split("/")[-1]



class SimulationQueueEntryState(models.Model):
  Waiting = 'Waiting'
  Executing = 'Executing'

class SimulationQueueEntry(models.Model):
  simulation_file = models.ForeignKey(SimulationFile)
  submit_time = models.DateTimeField('submission_time', default=datetime.datetime.now)
  simulation_start_time = models.DateTimeField(null=True, default=None)
  status = models.CharField(max_length=1000, default=SimulationQueueEntryState.Waiting )


  def get_simulation_time(self):
    return datetime.datetime.now() - self.simulation_start_time

  
