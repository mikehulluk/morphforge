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
import numpy as np
from morphforge.core.quantities.fromcore import unit
import quantities as pq

from morphforge.traces import TagSelector

class PlotSpec(object):
   
    def plot(self, ax, all_traces, time_range=None ) :
        raise NotImplementedError()
        



class PlotSpec_MixinTraceSelector(PlotSpec):
    def __init__(self, ylabel=None, **kwargs):
        super(PlotSpec_MixinTraceSelector, self).__init__(**kwargs)
        self.ylabel = ylabel or ""
    
    
    def addtrace_predicate(self, trace, ):
        raise NotImplementedError()

    def get_selector_ylabel(self):
        return self.ylabel
    
    
class PlotSpec_MixinPlotter(PlotSpec):

    def plot(self, ax, all_traces, time_range=None ) :
        raise NotImplementedError()
    






def default_legend_labeller(tr):
    if tr.comment:
        return tr.comment
    elif tr.name:
        return tr.name
    else:
        return None









class PlotSpecRegular(PlotSpec):
    
    def __init__(self, yrange=None, title=None, legend_labeller=default_legend_labeller, colors=None, yunit=None, event_marker_size=None):
        self.title = title
        self.yrange = yrange 
        self.legend_labeller = legend_labeller
        self.colors = colors
        
        self.yunit = yunit
        self.event_marker_size = event_marker_size
    

        
    def sort_traces(self, traces):
        return sorted( traces, key=lambda t : t.name)
    
    def sort_eventsets(self, event_sets):
        return sorted( event_sets, key=lambda t : t.name)
    

    def plot_trace(self, trace, time_range, ax, index, color=None):
        plot_kwargs = {}
        
        
        if self.legend_labeller is not None:
            plot_kwargs['label'] = self.legend_labeller(trace)
        
        
        if color is not None:
            plot_kwargs['color'] = color
        else:
            if self.colors:
                plot_kwargs['color'] = self.colors[ index % len(self.colors) ] 
                 
        pltTr =  ax.plotTrace(trace, **plot_kwargs)
        return pltTr

    def plot_eventset(self, eventset, time_range, ax, index):
        if len(eventset) == 0:
            return []
        
        
        plot_kwargs = {}
        if self.event_marker_size:
            plot_kwargs['markersize'] = self.event_marker_size        

        if self.legend_labeller is not None:
            plot_kwargs['label'] = self.legend_labeller(eventset)
        
        
        if 'label' in plot_kwargs:
            assert isinstance(plot_kwargs['label'], basestring)
            
        iRange = 0.2
        iScale = iRange / len( list(eventset.times) )
        
        data = np.array( [ (t.rescale("ms").magnitude,index+i*iScale) for i,t in enumerate(eventset.times) ] )
        
        
        
        from morphforge.stdimports import pq
        p= ax.plot( data[:,0] * pq.ms, data[:,1] * pq.dimensionless ,'x', **plot_kwargs )
        return p
        
        


    def plot(self, ax, all_traces,  all_eventsets,  time_range=None, linkage=None ) :

        # Which traces are we plotting (rely on a mixon class):
        trcs = [tr for tr in all_traces if self.addtrace_predicate(tr)]
        eventsets = [tr for tr in  all_eventsets if self.addeventset_predicate(tr)] 
        
               
        # Sort and plot:
        for index, trace in enumerate( self.sort_traces(trcs) ): 
            color = linkage.color_allocations.get(trace, None) if linkage else None
            self.plot_trace( trace, time_range=time_range, ax=ax, index=index, color=color)
        
            
        for index, event_set in enumerate( self.sort_eventsets(eventsets) ): 
            self.plot_eventset( event_set, time_range=time_range, ax=ax, index=index+len(trcs) )
            
            #ax.set_ylim( ( (-0.5) * pq.dimensionless, (len(eventsets)+0.5) * pq.dimensionless ) )
        
        
        if len(trcs) == 0:
            padding =0.5
            ax.set_yunit( 1*pq.dimensionless )
            ax.set_ylim( ( (-padding) * pq.dimensionless, (len(eventsets)-1+padding) * pq.dimensionless ) )
        
        #Legend:
        if self.legend_labeller is not None:
            import math
            import __builtin__ as BI
            ncols = BI.max( int( math.floor( len(trcs) / 10.0) ), 1)
            ax.legend(ncol=ncols)

        if self.title:
            ax.set_title( self.title )
            
        # Label up the axis:        
        ax.set_xlabel('Time')
        ax.set_xunit( unit('ms') )
        
        ax.set_ylabel( self.get_selector_ylabel() )
        
        if time_range is not None:
            print 'Setting Time Range', time_range
            ax.set_xlim( time_range )
        if self.yrange is not None:
            ax.set_ylim( self.yrange )

        if self.yunit is not None:
            print 'Setting Yunit', self.yunit
            ax.set_display_unit(y=self.yunit)
        
        # Turn the grid on:
        ax.grid('on')

        
        
        


class PlotSpec_Selector_StringTags(PlotSpec_MixinTraceSelector):
    def __init__(self, s, **kwargs):
        super(PlotSpec_Selector_StringTags,self).__init__(**kwargs)
        
        if isinstance(s, TagSelector):
            self.selector = s
        elif isinstance(s, basestring):
            self.selector = TagSelector.fromString(s)
        else:
            assert False
            
    
    def addtrace_predicate(self, trace):
        return self.selector(trace)
    def addeventset_predicate(self, trace):
        return self.selector(trace)



#class PlotSpec_ANDTags(PlotSpec_MixinTraceSelector):
#    def __init__(self, tags, **kwargs):
#        super(PlotSpec_ANDTags,self).__init__(**kwargs)
#        self.tags = tags
#        
#    def addtrace_predicate(self, trace):
#        
#        for tag in self.tags:
#            if not tag in trace.tags:
#                return False
#        return True
#    
#    def addeventset_predicate(self, eventset):
#        
#        for tag in self.tags:
#            if not tag in eventset.tags:
#                return False
#        return True
#    
#    
#    def get_selector_ylabel(self):
#         return "-".join(self.tags)
     


class PlotSpec_DefaultNew(PlotSpec_Selector_StringTags, PlotSpecRegular):
    def __init__(self, **kwargs):
        super(PlotSpec_DefaultNew,self).__init__(**kwargs)



#class PlotSpec_Default(PlotSpec_ANDTags, PlotSpecRegular):
#    def __init__(self, **kwargs):
#        super(PlotSpec_Default,self).__init__(**kwargs)

