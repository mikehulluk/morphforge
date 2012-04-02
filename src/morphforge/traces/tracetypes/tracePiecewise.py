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
#from morphforge.core.quantities.fromcore import unit
from morphforge.traces.trace import Trace

import numpy as np
import itertools

#from morphforge.core.quantities import unit




class PieceWiseComponentVisitor(object):
    
    @classmethod
    def Visit(cls, o, **kwargs):
        return o.AcceptVisitor(cls,**kwargs)


    @classmethod
    def visit_linear(cls, o, **kwargs):
        raise NotImplementedError()

    @classmethod
    def visit_flat(cls, o, **kwargs):
        raise NotImplementedError()




class TracePieceFunction(object):
    
    def __init__(self, time_window):
        self.time_window = time_window
    
    def getMinTime(self):
        return self.time_window[0]

    def getMaxTime(self):
        return self.time_window[1]

    def getDuration(self):
        return self.getMaxTime() - self.getMinTime()    
    

    def geStartValue(self):
        raise NotImplementedError()
    def getEndValue(self):
        raise NotImplementedError()

    # To allow for manipulation: 
    def AcceptVisitor(self):
        assert False
        
    
    
        
        
        
class TracePieceFunctionLinear(TracePieceFunction):
    def __init__(self, time_window, x0=None, x1=None):
        assert x0 is not None and x1 is not None
        
        TracePieceFunction.__init__(self, time_window=time_window)
        self.x0 = x0
        self.x1 = x1
        
    def AcceptVisitor(self, visitor, **kwargs):
        return visitor.visit_linear(self, **kwargs) 
        
    def getStartValue(self):
        return  self.x0
    def getEndValue(self):
        return  self.x1



class TracePieceFunctionFlat(TracePieceFunction):
    def __init__(self, time_window, x=None,):
        TracePieceFunction.__init__(self, time_window=time_window)
        assert x is not None
        self.x = x
        
    def getValue(self):
        return self.x
    
         
    def getValues(self, times):
        return np.ones( len(times) ) * self.x

    def getStartValue(self):
        return  self.x
    def getEndValue(self):
        return  self.x
    
    def AcceptVisitor(self, visitor, **kwargs):
        return visitor.visit_flat(self, **kwargs) 
    


class Trace_Piecewise(Trace):
    def __init__(self, pieces,name=None, comment=None, tags=None):
        Trace.__init__(self, name=name, comment=comment, tags=tags)
        self._pieces = pieces
    
        # Check we link up:
        for i in range( len(pieces) -1 ):
            dist = self._pieces[i].getMaxTime() - self._pieces[i+1].getMinTime()
            #print dist
            assert np.fabs( dist.rescale('ms').magnitude ) < 0.001
        
        
            
    def getMinTime(self):
        return self._pieces[0].getMinTime()

    def getMaxTime(self):
        return self._pieces[-1].getMaxTime()
    
    def nPieces(self):
        return len(self._pieces)
    
    def nPiecesLongerThan(self, t):
        return len( [ p for p in self._pieces if p.getDuration() > t] )
        
    
    def getValues(self, times):
        #from morphforge.core.quantities import unit
        _datas = []
        _times =[]
        assert (times <= self.getMaxTime() ).all()
        assert (times >= self.getMinTime() ).all()
        doneTimes = np.ones( len(times) ) > 0.0
        for p in self._pieces:
            ind1 = (times.rescale('ms') < float(p.getMaxTime().rescale('ms').magnitude) )
            ind = np.logical_and(ind1,doneTimes)
            indLocs = np.where(ind)
            
            _time = times[indLocs]
            _data = p.getValues(_time)
            _datas.append(_data)
            _times.append(_time)
            
            # Only visit these times once:
            doneTimes = np.logical_and( doneTimes, np.logical_not(ind) )
    
        unit  = _data[0].units
        return np.fromiter( itertools.chain(*[ list(d.rescale(unit).magnitude) for d in _datas]), dtype=np.float ) * unit
