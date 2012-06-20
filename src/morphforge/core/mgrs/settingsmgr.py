#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
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
import os


class SettingsMgr(object):
    """ Doc String for Settings Manager"""
    _showGui = True
    _showAllPlots = True
    
    # Don't Start Logging until everything is Configured!
    _logging = True and False

    _clearTempAllAtStart = True
    _simulateWithMocks = False

    # Query Settings:
    @classmethod
    def showGUI(cls):
        assert False
        if os.environ.get('MF_PLOT',None) == 'OFF':
            return False
        if os.environ.get('MF_BATCH',None):
            return False
        return  cls._showGui
    
    @classmethod
    def showAllPlots(cls):
        return cls._showAllPlots and cls._showGui 

    @classmethod
    def isLogging(cls):
        return cls._logging 
    
    @classmethod
    def mockSimulation(cls):
        return cls._simulateWithMocks        

    @classmethod
    def clearAllTempAtStart(cls):
        if os.environ.get('MF_BATCH',None):
            return True
        return cls._clearTempAllAtStart

    @classmethod
    def setCoverageRun(cls):
        assert False
        from logmgr import LogMgr
        LogMgr.info("Setting Coverage Run")
        cls._showGui = False
    
    @classmethod
    def allowEvalInLoading(cls):
        assert False
        return False
    
    @classmethod
    def DecorateSimulations(cls):
        assert False
        if os.environ.get('MF_BATCH',None):
            return True
        return False


    @classmethod
    def tagViewerAutoShow(cls):
        return True

    @classmethod
    def getPLYLexDebugFlag(cls):
        return 0
    
    @classmethod
    def getPLYYaccDebugFlag(cls):
        return 0
    
    
    @classmethod
    def SimulatorIsVerbose(cls):
        return False
