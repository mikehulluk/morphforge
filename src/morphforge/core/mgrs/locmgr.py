#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.  
#  - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation 
#  and/or other materials provided with the distribution.
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
import os
import time
import socket



from os.path import exists as Exists
from os.path import normpath as Normpath
from os.path import join as Join

from shutil import move as Move

import random
from datetime import datetime 




class LocMgr(object):

    locations = {}
    
    def __init__(self):
        pass
        
        
    @classmethod
    def ValidateExists(cls, location):
        """ Helper function to ensure that returned path actually does exist"""
        if location and not Exists(location): raise ValueError("Directory does not exist: %s"% location)
        return location
    
    @classmethod
    def EnsureMakeDirs(cls, location):
        """ Helper function that will make directories if they don't exist. Useful for temporary locations""" 
        
        if location and not Exists(location): 
            from logmgr import LogMgr
            LogMgr.info("Creating FS Location - " + location)
            if  not Exists(location): os.makedirs(location)
        return cls.ValidateExists(location)
        
    
    
        
    @classmethod
    def getRootPath(cls):
        # Load it from the .rc file:
        if not "rootdir" in cls.locations:
            cls.locations["rootdir"] = os.path.abspath( os.path.join( os.path.dirname(__file__), "../../../" ) )
            cls.ValidateExists(cls.locations["rootdir"])
            
        return cls.ValidateExists(cls.locations["rootdir"]) 

    @classmethod
    def getSubLibraryPath(cls, ):
        return cls.ValidateExists(Join(cls.getRootPath(), "../sublibraries/"))
    
      
    @classmethod
    def getBinPath(cls):
        return cls.ValidateExists(Join(cls.getRootPath(), "bin/"))  
    
    @classmethod
    def getLogPath(cls):
        return cls.EnsureMakeDirs(Join(cls.getTmpPath(), "log/"))

    @classmethod
    def getDatabaseConfigFile(cls):
        return cls.ValidateExists(Join(cls.getRootPath(), "etc/databases.yaml"))
    
    @classmethod
    def getDefaultDatabaseNameFile(cls):
        return cls.ValidateExists(Join(cls.getRootPath(), "etc/current_db"))
    
    
    
    
    
    
    @classmethod
    def getTemporaryFilename(cls, suffix="", filedirectory=None):
        from morphforge.core.misc import getStringMD5Checksum

        rndString = "%f%d%s" % (time.time(), random.randint(0, 32000), socket.gethostname())
        fn = "tmp_%s%s" % (getStringMD5Checksum(rndString), suffix)
        
        filedirectory = filedirectory if filedirectory else cls.getTmpPath()
        return Join(filedirectory, fn)
        
    
    
    @classmethod
    def removeAllTemporaryFiles(cls):
        curDataStr = datetime.today().strftime("%y_%m_%d_%H_%M_%S")
        newDir = Join(cls.getTmpBackupPath(), "tmp_" + curDataStr)
        Move(LocMgr.getTmpPath(), newDir)
        
        
    
    @classmethod
    def loadFromRCReader(cls, subsection, default):
        from rcmgr import RCMgr
        if not RCMgr.hasConfig():
            return default
        
        if not subsection in cls.locations:
            
            if RCMgr.has("Locations", subsection): 
                cls.locations[subsection] = RCMgr.get("Locations", subsection)
            else:
                cls.locations[subsection] = default
                
        cls.locations[subsection] = cls.locations[subsection].replace("${PID}", "%d" % os.getpid())
        return cls.EnsureMakeDirs(cls.locations[subsection])
    
        
    
    @classmethod
    def getTmpPath(cls):
        try:
            loc = cls.loadFromRCReader("tmpdir", Join(cls.getRootPath(), "tmp"))
        except:
            loc = Join(cls.getRootPath(), "tmp")
        return cls.EnsureMakeDirs(loc)
    
    
    @classmethod
    def getTmpBackupPath(cls):
        return cls.EnsureMakeDirs(Join(cls.getRootPath(), "tmpbackup"))
    
    @classmethod 
    def getCoveragePath(cls):
        return cls.EnsureMakeDirs(Join(cls.getTmpPath(), "coverage"))
    
    
    @classmethod
    def getDefaultModBuildDir(cls):
        loc = cls.loadFromRCReader("tmp_nrn_mod_builddir", Join(cls.getTmpPath(), "modbuild_%d/"%os.getpid()) )
        return cls.EnsureMakeDirs(loc)
        
        
    @classmethod
    def getDefaultModOutDir(cls):
        loc = cls.loadFromRCReader("tmp_nrn_mod_buildout", Join(cls.getTmpPath(), "modout/"))
        return cls.EnsureMakeDirs(loc)
        
    
    @classmethod
    def getDefaultOutputDir(cls):
        loc = Join( cls.getRootPath(), "output")
        return cls.EnsureMakeDirs(loc)
    
    
    @classmethod
    def getDefaultSummaryOutputDir(cls):
        loc = Join( cls.getDefaultOutputDir(), "summaries")
        return cls.EnsureMakeDirs(loc)
    
    @classmethod
    def getDefaultChannelSummaryOutputDir(cls):
        loc = Join( cls.getDefaultSummaryOutputDir(), "channels" )
        return cls.EnsureMakeDirs(loc)
    
    
    
    
    
    
    @classmethod
    def getSimulationTmpDir(cls):
        loc = cls.loadFromRCReader("tmp_simulationpicklesdir", Join(cls.getTmpPath(), "simulationdir"))
        return cls.EnsureMakeDirs(loc)
             

    
    @classmethod
    def getSimulationResultsTmpDir(cls):
        loc = cls.loadFromRCReader("tmp_simulationpicklesdir", Join(cls.getTmpPath(), "simulationresults"))
        return cls.EnsureMakeDirs(loc)
    
    
    
    @classmethod
    def getSimulationResultsDBDir(cls):
        loc = cls.loadFromRCReader("simulationdbresultsdir", Join(cls.getRootPath(), "dbData/"))
        return cls.EnsureMakeDirs(loc)
    
    @classmethod
    def getJobSimDBDir(cls):
        loc = cls.loadFromRCReader("jobsimdir", Join(cls.getRootPath(), "dbData/"))
        return cls.EnsureMakeDirs(loc)
    
    
    
    @classmethod
    def BackupDirectory(cls, location):
        assert Exists(location)
        
        cleanLoc = Normpath(location)
        if cleanLoc.endswith("/"): cleanLoc = cleanLoc[:-1] 
        
        def backLoc(l, suffix): return l + "_backup%d" % suffix
        
        suffix = 1
        while Exists(backLoc(cleanLoc, suffix)): suffix = suffix + 1
        newLoc = backLoc(cleanLoc, suffix)
        Move(location, newLoc)
    
    
    @classmethod
    def getPLYParseTabLocation(cls, subdir=None):
        #username = os.getuid()
        
        #dir_name = '/tmp/morphforge_%d/parsetabs/'%username
        dir_name = os.path.join( cls.getTmpPath(), "parsetabs/")
        
        if not subdir:
            assert False
            return cls.EnsureMakeDirs(dir_name)
        else:
            return cls.EnsureMakeDirs( os.path.join( dir_name, subdir) )




    ## Test Data:
    ######################
    
    
    
    
    @classmethod
    def getTestSrcsPath(cls):
        return cls.ValidateExists(Join(cls.getRootPath(), "../test_data"))
    
    @classmethod
    def getTestEqnSetsPath(cls):
        return cls.ValidateExists(Join(cls.getTestSrcsPath(), "eqnset"))
    
    @classmethod
    def getTestModsPath(cls):
        return cls.ValidateExists(Join(cls.getTestSrcsPath(), "test_mods"))
    
    @classmethod
    def getTestParamDataPath(cls):
        return cls.ValidateExists(Join(cls.getTestSrcsPath(), "hoc_params"))

    @classmethod
    def getYAMLMorphDataPath(cls):
        return cls.ValidateExists(Join(cls.getTestSrcsPath(), "morph_yamls"))

    @classmethod
    def getYAMLMembranePropertiesPath(cls):
        return cls.ValidateExists(Join(cls.getTestSrcsPath(), "membrane_parameters"))
     
     
    @classmethod
    def getYAMLCellsPath(cls):
        return cls.ValidateExists(Join(cls.getTestSrcsPath(), "cell_yamls"))
     

    @classmethod
    def getGraphDefaultOutputPath(cls):
        return cls.EnsureMakeDirs(Join(cls.getTmpPath(), "graphs/"))

    @classmethod
    def getDocOutputPath(cls):
        return cls.EnsureMakeDirs(Join(cls.getTmpPath(), "docOutput/"))
