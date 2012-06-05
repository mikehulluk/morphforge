##-------------------------------------------------------------------------------
## Copyright (c) 2012 Michael Hull.  All rights reserved.
## 
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
## 
##  - Redistributions of source code must retain the above copyright notice,
##  this list of conditions and the following disclaimer.  - Redistributions in
##  binary form must reproduce the above copyright notice, this list of
##  conditions and the following disclaimer in the documentation and/or other
##  materials provided with the distribution.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE.
##-------------------------------------------------------------------------------
#
#from utils import *  
#
#from plotmanager import PlotManager
#
#class SimulationMgr(object):
#    
#    @classmethod
#    def InitStandard(cls):
#        ScriptUtils.updateLinkToOutputDir()
#        opDir = ScriptUtils.getOutputDir()
#        
#        os.chdir(opDir)
#        
#        # Store data about the repos:
#        #cls.getRepositoryStatus("/home/michael/hw/morphforge/")
#        #cls.getRepositoryStatus("/home/michael/hw/signalanalysis/")
#        
#        #
#        PlotManager.defaultFilenameTmpl = """fig{fignum:d}_{figname}.{figtype}"""
#        
#       
#    @classmethod 
#    def getRepositoryStatus(cls, repoLocation):
#        assert False, "Mike Hull specific code!"
#        detailsFile = "RepoStatus_" +  repoLocation.split("/")[-2] + ".txt"
#        
#        argStr = "hg -R %s summary" % repoLocation
#        os.system("echo 'Summary' >> %s" % detailsFile)
#        os.system("echo '-------' >> %s" % detailsFile)
#        os.system(argStr + " >> %s" % detailsFile)
#        
#        argStr = "hg -R %s status" % repoLocation
#        os.system("echo '\nStatus' >> %s" % detailsFile)
#        os.system("echo '-------' >> %s" % detailsFile)
#        os.system(argStr + " >> %s" % detailsFile)
#        
#        argStr = "hg -R %s diff" % repoLocation
#        os.system("echo '\nDiff' >> %s" % detailsFile)
#        os.system("echo '-------' >> %s" % detailsFile)
#        os.system(argStr + " >> %s" % detailsFile)
#
#

