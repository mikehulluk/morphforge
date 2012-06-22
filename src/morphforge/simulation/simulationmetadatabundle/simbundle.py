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

from morphforge.core import FileIO
from os.path import join as Join
from morphforge.core import LocMgr
from morphforge.core.misc import StrUtils


 
import cPickle



# This class is a work around for the circular loop caused by not being able to store the md5 hash of an object 
# within that object:

class SimMetaDataBundleBase(object):
    
    def __init__(self, sim):
        super(SimMetaDataBundleBase, self).__init__(sim=sim)
        self.simmd5sum = StrUtils.get_hash_md5(cPickle.dumps(sim))
        self.postsimulationactions = []
        
    def addPostProcessingAction(self, action):
        self.postsimulationactions.append(action)
    
    def doPostProcessingActions(self):
        assert self.getSimulation().result
        for action in self.postsimulationactions:
            action(self.getSimulation().result, self)
            
    @classmethod
    def loadFromFile(cls, filename):
        bundle = cPickle.load(open(filename))
        return bundle


    def getSimMD5Sum(self):
        return self.simmd5sum








class MixinSimLoc_AsObject(object):
    def __init__(self, sim):
        self.sim = sim
        
    def getSimulation(self):
        return self.sim
    
    def simLoc_Prepare(self):
        pass
    
    
class MixinSimLoc_AsFile(object):
    def __init__(self, sim, location=LocMgr.get_simulation_tmp_dir(), suffix=".neuronsim.pickle"):
        
        super(MixinSimLoc_AsFile, self).__init__()
        
        self.location = location
        self.suffix = suffix
        self.picklestring = cPickle.dumps(sim)

        self.simfilename = None
        self.sim_postload = None
    

            
    def getFilename(self):
        if not self.simfilename:
            simlocationWithDir = LocMgr.ensure_dir_exists(self.location + self.getSimMD5Sum()[0:1])
            simfileShort = self.getSimMD5Sum() + self.suffix
            self.simfilename = Join(simlocationWithDir, simfileShort)
        return self.simfilename
        
    def simLoc_Prepare(self):
        FileIO.write_to_file(txt=self.picklestring, filename=self.getFilename()) 
        self.picklestring = None
        
    def getSimulation(self):
        if not self.sim_postload:
            self.sim_postload = cPickle.load(open(self.simfilename))
        return self.sim_postload                                
            
    

class SimMetaDataBundle(SimMetaDataBundleBase, MixinSimLoc_AsObject):

#class SimMetaDataBundle(SimMetaDataBundleBase, MixinSimLoc_AsFile):
    
    def __init__(self, sim):
        
        super(SimMetaDataBundle, self).__init__(sim=sim)
        
        self.metadata = {}
        self.prepare()
        
            
    def prepare(self):
        self.simLoc_Prepare()
    
    
    
    
    
    def writeToFile(self, bundlefilename=None):
        bundleloc = LocMgr.get_simulation_tmp_dir()
        bundlesuffix = ".bundle"
        
        if not bundlefilename:            
            loc = bundlefilename = LocMgr.ensure_dir_exists(bundleloc + "/" + self.getSimMD5Sum()[0:2])
            bundlefilename = loc + "/" + self.getSimMD5Sum() + bundlesuffix
            #print "Bundle Filename", bundlefilename

        FileIO.write_to_file(txt=cPickle.dumps(self) , filename=bundlefilename)
        return bundlefilename
        
    def writeToFileAndGetExecString(self, bundlefilename=None, simBinFile="SimulateBundle.py"):
        
        bundlefilename = self.writeToFile(bundlefilename=bundlefilename)
        simCmd = Join(LocMgr.get_bin_path(), simBinFile) + " " + bundlefilename
        return bundlefilename, simCmd
        
        
        
        
        
        
        
        
