

from morphforge.simulationanalysis.summaries.mmsummariser import MembraneMechanismSummariser
from morphforge.core import LocMgr

import morphforgecontrib
import modelling.rbmodelling2 


loc = LocMgr. getDefaultChannelSummaryOutputDir()
MembraneMechanismSummariser.SummariseAll(loc)