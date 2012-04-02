#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.  - Redistributions in
#  binary form must reproduce the above copyright notice, this list of
#  conditions and the following disclaimer in the documentation and/or other
#  materials provided with the distribution.
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
import inspect
import os

from os.path import basename as Basename
from os.path import splitext as SplitExt

from os.path import dirname as DirName
from os.path import exists as Exists
from os.path import join as Join



import datetime
class ScriptUtils(object):
    
    
    # We store the Full iso format of when the simulation was run, as
    # well as the shortedn
    now = datetime.datetime.now()
    datetimestringISO = now.isoformat()
    datetimestringInformal = now.strftime("[%a %d %B - %I:%M]")
    datetimestr = "%s_%s/"%( datetimestringISO, datetimestringInformal )
    
    
    outputStoreDir = "_output_store/"
    currentOutputLinkDir =  "_out"
    
    @classmethod
    def getCallingScript(cls):
        frame = inspect.stack()
        
        calleeFrame = frame[-1]
        calleeFile = calleeFrame[1]
        return calleeFile 
         
    @classmethod
    def getCallingScriptDirectory(cls):
        return  DirName( cls.getCallingScript() )
    
    @classmethod
    def getCallingScriptFile(cls, includeExt):
        fName = Basename( cls.getCallingScript() )
        if includeExt:
            return fName
        else:
            return SplitExt(fName)[0]
        
        
        
        
        
    @classmethod
    def getOutputDir(cls):
        dirName = cls.outputStoreDir + cls.datetimestr
        fullDirName = Join( cls.getCallingScriptDirectory(), dirName )
        EnsureDirectoryExists(fullDirName)
        return fullDirName 
    
    
    @classmethod
    def updateLinkToOutputDir(cls):
        opDir = cls.getOutputDir()
        fullLinkName = Join( cls.getCallingScriptDirectory(), cls.currentOutputLinkDir )
        if Exists( fullLinkName ):
            os.unlink( fullLinkName )
        
        os.system("""ln -s "%s" "%s" """%(opDir, fullLinkName) )
        
        
def CleanFilename(f):
    f = f.replace("__","_")
    f = f.replace("_.",".")
    f = f.replace("\n","--")
    return f

def EnsureDirectoryExists(fName):
    d = DirName(fName)
    if not Exists(d) and d.strip():
        os.makedirs(d)
    
    
    
    
