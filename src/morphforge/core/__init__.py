#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
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


# First thing to do; monkey patch 
# external libraries like matplotlib, mayavi, numpy.
import monkey_patching
#monkey_patching.my_pass()



from mfrandom import MFRandom


from mgrs import LocMgr, LogMgr, SettingsMgr,  RCMgr 

from misc import WriteToFile, MergeDictionaries, ReadFile, AppendToFile, FilterExpectSingle, Flatten, CheckValidName, ExactlyOneNotNone, FilterWithProb
from misc import require, requiresubclass, CheckType, getFileMD5Checksum, getStringMD5Checksum, WriteStringToMD5SumName, ExecCommandGetRetCode, ExpectSingle
from misc import CleanName, TimerPredictor, isIterable


from mockcontrol import MockControl

from objectnumberer import ObjectLabeller


from os.path import split as Split
from os.path import join as Join
from os.path import exists as Exists
from os.path import dirname as Dirname
from os.path import basename as Basename



from plugindict import PluginDict



__all__ = [
    "LocMgr",
    "LogMgr",
    "SettingsMgr",
    "RCMgr",
    "WriteToFile",
    "MergeDictionaries",
    "ReadFile",
    "AppendToFile",
    "FilterExpectSingle",
    "FilterWithProb",
    "Flatten",
    "CheckValidName",
    "ExactlyOneNotNone",
    "require",
    "requiresubclass",
    "CheckType",
    "getFileMD5Checksum",
    "getStringMD5Checksum",
    "WriteStringToMD5SumName",
    "ExecCommandGetRetCode",
    "ExpectSingle",
    "CleanName",
    "TimerPredictor",
    "isIterable",
    "ObjectLabeller",
    "Split",
    "Join",
    "Exists",
    "Dirname",
    "Basename",
    "PluginDict",
    "MFRandom",
    "MockControl",
]


