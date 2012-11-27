

import morphforge.stdimports as mf

from ..core import StdChlAlphaBeta

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




def plot_sv(ax, sv_name, sv_coeffs, what, plot_kwargs=None):
    assert what in ['alpha','beta','tau','inf']

    SV = sv_coeffs
    v = np.linspace(-80,50,100)
    alpha = (SV[0][0] + SV[0][1] * v) / ( SV[0][2] + np.exp( (SV[0][3] + v ) / SV[0][4] ))
    beta  = (SV[1][0] + SV[1][1] * v) / ( SV[1][2] + np.exp( (SV[1][3] + v ) / SV[1][4] ))

    inf = alpha/(alpha+beta)
    tau = 1.0/(alpha+beta)

    vals = { 'alpha':alpha,
            'beta':beta,
            'inf':inf,
            'tau':tau,
            }[what]

    plot_kwargs = plot_kwargs or {}
    return ax.plot(v, vals, label=sv_name ,**plot_kwargs)


class AlphaBetaSummariser(object):
    pass

    @classmethod
    def build(cls, obj):
        pass
        param_tbl= mrd.VerticalColTable( ['Parameter','Value'],
                [
                    ('Conductance (gmax)', str(obj.conductance.rescale('mS/cm2')) ),
                    ('Reversal Potential', str(obj.reversalpotential.rescale('mV'))),
                 ] )


        sv_tbls = []
        for sv in obj.statevars:
            sv_table = mrd.VerticalColTable( ['$%s$'%sv,'A','B','C','D','E'],
                   (  ['Alpha'] +[str(f) for f in  obj.statevars[sv][0]],
                      ['Beta'] + [str(f) for f in  obj.statevars[sv][1]],
                       ) )
            sv_tbls.append(sv_table)

        sv_eqns = []
        sv_eqns.append( r"""\frac{d}{dt}%s &= \frac{%s_\infty(V) - %s}{\tau_{%s}(V)}""".replace('%s','SV') )
        sv_eqns.append( r"""%s_\infty(V) &= \frac{\alpha_{%s}(V)}{\alpha_{%s}(V) + \beta_{%s}(V)}""".replace('%s','SV') )
        sv_eqns.append( r"""\tau_{%s}(V) &= \frac{1.0}{\alpha_{%s}(V) + \beta_{%s}(V)}""".replace('%s','SV') )
        sv_eqns.append( r"""\alpha_{%s}(V),\beta_{%s}(V)  &= \frac{A + BV}{C + exp(\dfrac{D+V}{E})} """.replace('%s','SV') )


        sv_fig = pylab.figure(figsize=(6,4))
        axes = {
        'alpha': sv_fig.add_subplot(2,2,1), 'beta':  sv_fig.add_subplot(2,2,2),
        'inf':   sv_fig.add_subplot(2,2,3), 'tau':   sv_fig.add_subplot(2,2,4),
        }

        for sv_name, sv_vars in obj.statevars.items():
            plot_sv(axes['alpha'], sv_name, sv_vars, 'alpha')
            plot_sv(axes['beta'] , sv_name, sv_vars, 'beta')
            plot_sv(axes['inf'] , sv_name, sv_vars, 'inf')
            plot_sv(axes['tau'] , sv_name, sv_vars, 'tau')

        for ax_name, ax in axes.items():
            ax.legend()
            ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(6))
            ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
            ax.set_ylabel(ax_name)

        set_fontsize(sv_fig, 8)

        return mrd.Section('Summary of %s (StdChlAlphaBeta)' % obj.name,
                mrd.EquationBlock(
                    mrd.Equation( 'g &= gmax * %s' % obj.eqn),
                    mrd.Equation( 'i &= g * (erev-V)' ),
                    ),
                mrd.EquationBlock(
                    *sv_eqns
                    ),
                param_tbl,
                sv_tbls,
                mrd.Image(sv_fig, auto_adjust=False),


                )


#assert False
mf.SummariserLibrary.register_summariser( StdChlAlphaBeta, AlphaBetaSummariser)


