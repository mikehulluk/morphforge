#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
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
from morphforge.core.quantities.fromcore import quantity_unit_to_string
import json


import numpy as np

class NeuroCSVWriter(object):
    
    @classmethod
    def write_to_file(cls, fileName, **kwargs):
        with open(fileName,'w') as f:
             return NeuroCSVWriter.write_to_buffer(fileObj=f, **kwargs)
    
    
    
    @classmethod
    def write_to_buffer(cls, fileObj, traces=None, event_sets=None, time_indices=None, csv_metadata=None  ):
        print 'Writing Out Traces:'
        traces=traces or []
        event_sets=event_sets or []
        
        #if not time_indices:
        #    assert False
        
        # Column Headers:
        colHeaders=[ cls.generate_column_header( tr,i) for i,tr in enumerate(traces) ]
        
        # Event Data:
        evtHeaders=[cls.generate_eventset_header(evset) for evset in event_sets]

        # Build the Header:
        header_meta = "" if csv_metadata is None else "!%s"%json.dumps(csv_metadata)
        header_cols = "\n".join(colHeaders)
        header_events = "\n".join( evtHeaders )
        header = "\n".join( [header_meta,header_cols, header_events] )
        
        
        
        
        
        # Build the Column Data:
        #time_indices = traces[0]._time
        
        col_width=10
        def missingFormat(): return "-".center(col_width)
        def dataFormat(d):    return ("%f"%d).ljust(col_width)
        
        colData = []
        for tr in traces:
            
            data = [missingFormat()] * len(time_indices)
            
            tr_valid_times_bool = tr.time_within_trace(time_indices)
            valid_time_indices = np.where(tr_valid_times_bool)[0]
            valid_time_data_vals = tr.getValues( time_indices[valid_time_indices] )
            
            for tIndex,data_val in zip(valid_time_indices, valid_time_data_vals ):
                data[tIndex] = dataFormat( float( data_val.magnitude ) )
            #tr_data= tr.getValues
            colData.append(data)
        
        
        
        # Write the header
        fileObj.write(header)
        fileObj.write("\n")
        
        # Write the data:
        for i,t in enumerate(time_indices):
            tStr = dataFormat(t)
            cStrings = [ cData[i] for cData in colData]
            l = "\t".join( [tStr] + cStrings ) 
            fileObj.write( l + "\n"  )
            
        
        
        #print header
        
    @classmethod
    def generate_column_header(self, tr, index):
        d = {'label':tr.name,
             'unit': quantity_unit_to_string( tr._data.units),
             'tags': ",".join( tr.tags ) 
             }
        s1 = "#! COLUMN%d: "%(index)
        s2 = json.dumps(d)
        return s1+s2
    
    @classmethod
    def generate_eventset_header(self, eventset):
        d = {'label':eventset.name,
             'tags': ",".join( eventset.tags ) 
             }
        s1 = "#@ EVENT %s "%json.dumps(d)
        s2 = " ".join( ["%2.2f"%e.getTime() for e in eventset] )
        return s1+s2
