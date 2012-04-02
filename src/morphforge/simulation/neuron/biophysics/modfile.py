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

from morphforge.core import getStringMD5Checksum, LocMgr, LogMgr, require

from os.path import join as Join
from morphforge.core.misc import ExpectSingle


class ModFile(object):


    
    @require("modtxt", str, unicode)
    def __init__(self, modtxt, name=None, additional_compile_flags="", additional_link_flags="", additional_LD_LIBRARY_PATH=""):
        self.name = name
        self.modtxt = modtxt
        
        # if no name is provided:
        if self.name == None:
            import re
            c = re.compile("""SUFFIX \W ([a-zA-Z]*) \W """, re.VERBOSE)
            m = c.findall(modtxt)
            self.name = ExpectSingle(m)
            
            #assert m and len(m) == 1
            #self.name = m[0]
           
        self.additional_compile_flags  = additional_compile_flags
        self.additional_link_flags = additional_link_flags
        self.additional_LD_LIBRARY_PATH = additional_LD_LIBRARY_PATH
            
       
    def ensureBuilt(self):
        LogMgr.info("Ensuring Modfile is built")
        from modfilecompiler import ModFileCompiler
        ModFileCompiler()._buildMODFile(self)
    
    
        
    def getMD5Hash(self):
        return getStringMD5Checksum(self.modtxt)
    
    
    
    def getBuiltFilenameShort(self, ensureBuilt=True):
        if ensureBuilt: self.ensureBuilt() 
        return "mod_" + self.getMD5Hash() + ".so"
    
    def getBuiltFilenameFull(self, ensureBuilt=True):
        if ensureBuilt: self.ensureBuilt()
        return Join(LocMgr.getDefaultModOutDir(), self.getBuiltFilenameShort(ensureBuilt=ensureBuilt))  
    
    
    
