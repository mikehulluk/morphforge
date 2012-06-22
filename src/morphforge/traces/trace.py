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
import operator
import functools




class Trace(object):
    def __init__(self, name, comment, tags):
        self.tags = [] if tags == None else tags
        self.name = name if name else '<Unnamed Trace>'
        self.comment = comment if comment else "UnknownSrc"

    # Forward operator functions to be looked up:    
    def __add__(self, rhs):
        from trace_operators_ctrl import TraceOperatorCtrl
        return TraceOperatorCtrl.operate(operator.__add__, lhs=self, rhs=rhs)
    def __sub__(self, rhs):
        from trace_operators_ctrl import TraceOperatorCtrl
        return TraceOperatorCtrl.operate(operator.__sub__, lhs=self, rhs=rhs)
    def __div__(self, rhs):
        from trace_operators_ctrl import TraceOperatorCtrl
        return TraceOperatorCtrl.operate(operator.__div__, lhs=self, rhs=rhs)
  
    def __mul__(self, rhs):
        from trace_operators_ctrl import TraceOperatorCtrl
        return TraceOperatorCtrl.operate(operator.__mul__, lhs=self, rhs=rhs)

    # Forward method lookup
    def __getattr__(self, name):
        from trace_methods_ctrl import TraceMethodCtrl
        
        if TraceMethodCtrl.has_method(self.__class__, name):
            func = TraceMethodCtrl.get_method(self.__class__, name)
            return functools.partial(func, self)
        raise AttributeError('No Such method for trace type: %s.%s.' % (self.__class__, name))
      

    # Subclasses must implement these:
    def get_min_time(self):
        raise NotImplementedError()

    def get_max_time(self):
        raise NotImplementedError()

    def get_value_at_time(self, time):
        print type(self)
        raise NotImplementedError()

    def time_within_trace(self, times):
        raise NotImplementedError()


    # Utility Functions:
    def get_duration(self):
        return self.get_max_time() - self.get_min_time()


