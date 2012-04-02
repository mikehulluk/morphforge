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
from tracetypes import *
# Base Classes:


#from trace import  Trace_PointBased
#from traceFixedDT import  Trace_FixedDT
#from traceVariableDT import  Trace_VariableDT
#from tracePiecewise import  Trace_Piecewise, TracePieceFunctionLinear, TracePieceFunctionFlat


# Conversion and splicing:
#from trace_conversion import  TraceConverter
from traceGenerator import TraceGenerator
#from traceLoader import TraceLoader

from eventset import * 


# Need so that they register the methods:
import std_methods
import std_operators


from tags import *


__all__ = [
"Trace_FixedDT",
#"TraceConverter",
"Trace_VariableDT",
"Trace_PointBased",
"Trace_Piecewise",
"TracePieceFunctionLinear",
"TracePieceFunctionFlat",
"TracePieceFunctionLinear",
#"TraceConverter",
"TraceGenerator",
#"TraceLoader",
"TagSelector",
"TagSelect",
]


