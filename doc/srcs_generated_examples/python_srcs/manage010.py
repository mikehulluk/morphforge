





from morphforge.stdimports import PluginMgr
import morphforgecontrib.stdimports as mfc

fname = '~/Desktop/morphforge_config.pdf'
summary = PluginMgr.summarise_all()
summary.to_pdf(fname)
print 'morphforge environment summary stored at: %s'%fname


