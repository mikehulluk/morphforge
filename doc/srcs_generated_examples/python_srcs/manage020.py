





import mredoc
from morphforge.stdimports import PluginMgr, CellLibrary, ChannelLibrary, MorphologyLibrary, PostSynapticTemplateLibrary
import morphforgecontrib.stdimports as mfc
from  modelling import *
from modelling.sensory_pathway import *
fname = '~/Desktop/morphforge_registered_templates.pdf'

mredoc.Section('Summary',
    CellLibrary.summary_table(),
    ChannelLibrary.summary_table(),
    MorphologyLibrary.summary_table(),
    PostSynapticTemplateLibrary.summary_table(),

    ).to_pdf(fname)

print 'Cell & Channel summary stored at: %s'%fname


