
import morphforge.stdimports as mf
from  morphforge.traces.generation  import TraceStringParser
import quantities as pq


tests = [
"""{d:pA} AT 0ms FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 120ms THEN FLAT(50) FOR 20ms """,
"""{d:pA} AT 0ms FLAT(0) UNTIL 150ms THEN FLAT(120) FOR 20ms THEN FLAT(0) FOR 20ms""",
"""{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 160ms""",
"""{d:pA} FLAT(1) FOR 100ms THEN RAMPTO(50) UNTIL 130ms THEN FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms""",
"""{d:pA} FLAT(0) THEN AT 150ms FLAT(120) FOR 20ms THEN  FLAT(0) UNTIL 180ms""",
 ]


for t in tests:
    tr = TraceStringParser.Parse(t)
    tr.tags = ['Current']

    tr2 = tr.convert_to_fixed(dt=0.1*pq.ms) *1.1
    tr2.tags = ['Current']

    tr3 = tr-tr2
    #tr = trace_from_string(t)
    mf.TagViewer([tr,tr2], figtitle=t)






