 import morphforge.stdimports as mf
 from sim_builtin_core import BuiltinChannel


class BuiltinChlSummariser(object):
    @classmethod
    def build(cls, obj):
        return mrd.Section('Summary of %s (Existing Modfile)' % obj.name,
               "(Builtin Channelcd )"
                )


mf.SummariserLibrary.register_summariser(BuiltinChannel, BuiltinChlSummariser)

