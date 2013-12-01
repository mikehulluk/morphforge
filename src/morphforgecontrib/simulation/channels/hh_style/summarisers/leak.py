


import morphforge.stdimports as mf

from ..core import StdChlLeak

import numpy as np
import pylab
import matplotlib as mpl


def set_fontsize(fig,fontsize):
    """
    For each text object of a figure fig, set the font size to fontsize
    """
    def match(artist):
        return artist.__module__ == "matplotlib.text"

    for textobj in fig.findobj(match=match):
        textobj.set_fontsize(fontsize)






class LeakSummariser(object):

    @classmethod
    def build(cls, obj):
        import mredoc as mrd
        param_tbl= mrd.VerticalColTable( ['Parameter','Value'],
                [
                    ('Conductance (gmax)', str(obj.conductance.rescale('mS/cm2')) ),
                    ('Reversal Potential', str(obj.reversalpotential.rescale('mV'))),
                 ] )




        return mrd.Section('Summary of %s (StdChlAlphaBeta)' % obj.name,
                mrd.EquationBlock(
                    mrd.Equation( 'g &= gmax ' ),
                    mrd.Equation( 'i &= g * (erev-V)' ),
                    ),
                param_tbl,


                )


mf.SummariserLibrary.register_summariser( StdChlLeak, LeakSummariser)


