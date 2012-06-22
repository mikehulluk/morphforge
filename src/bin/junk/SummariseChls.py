

from morphforge.simulationanalysis.summaries.mmsummariser import MembraneMechanismSummariser
from morphforge.core import LocMgr

import morphforgecontrib
import modelling.rbmodelling2 


loc = LocMgr. get_default_channel_summary_output_dir()
MembraneMechanismSummariser.summarise_all(loc)