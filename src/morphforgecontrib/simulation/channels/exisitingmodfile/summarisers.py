
import morphforge.stdimports as mf

from core import SimulatorSpecificChannel

class ExistingModfileSummariser(object):

    @classmethod
    def build(cls, obj):
        import mredoc as mrd
        return mrd.Section('Summary of %s (Existing Modfile)' % obj.name,
               mrd.VerbatimBlock(obj.mod_text)
                )

mf.SummariserLibrary.register_summariser( SimulatorSpecificChannel, ExistingModfileSummariser)


