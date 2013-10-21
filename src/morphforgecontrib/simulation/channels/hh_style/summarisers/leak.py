


import morphforge.stdimports as mf

from ..core import StdChlLeak

import mredoc as mrd
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




#def plot_sv(ax, sv_name, sv_coeffs, what, plot_kwargs=None):
#    assert what in ['alpha','beta','tau','inf']
#
#    SV = sv_coeffs
#    v = np.linspace(-80,50,100)
#    alpha = (SV[0][0] + SV[0][1] * v) / ( SV[0][2] + np.exp( (SV[0][3] + v ) / SV[0][4] ))
#    beta  = (SV[1][0] + SV[1][1] * v) / ( SV[1][2] + np.exp( (SV[1][3] + v ) / SV[1][4] ))
#
#    inf = alpha/(alpha+beta)
#    tau = 1.0/(alpha+beta)
#
#    vals = { 'alpha':alpha,
#            'beta':beta,
#            'inf':inf,
#            'tau':tau,
#            }[what]
#
#    plot_kwargs = plot_kwargs or {}
#    return ax.plot(v, vals, label=sv_name ,**plot_kwargs)


class LeakSummariser(object):
    pass

    @classmethod
    def build(cls, obj):
        pass
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


#assert False
mf.SummariserLibrary.register_summariser( StdChlLeak, LeakSummariser)


