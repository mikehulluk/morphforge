

from core import PostSynapticMech_Exp2Syn_Base
import morphforge.stdimports as mf


class PostSynapticMech_Exp2Syn_BaseSummariser(object):

    @classmethod
    def build(cls, obj):
        import mredoc as mrd
        # Create the parameter table:
        parameter_table = mrd.VerticalColTable( ('Parameter','Value'),
                   [
                      (k,str(v)) for (k,v) in sorted( obj.get_defaults().items() )
                   ]
        )
        
        eqns = [
            mrd.Equation(r"""i &= g_{peak}  * (B-A) * \frac{1}{tc_{max}} * (V-E_{rev})"""),
            mrd.Equation(r"""\frac{d}{dt}A &= -A / tau_{open}"""),
            mrd.Equation(r"""\frac{d}{dt}B &= -B / tau_{close} """),
            mrd.Equation(r"""t_{max} &= ln(\tau_{close} / \tau_{open}) * (\tau_{open} * \tau_{close}) / (\tau_{close} - \tau_{open})"""),
            mrd.Equation(r"""tc_{max} &= exp( -t_{max} / tc_close) -  exp( -t_{max}/ tc_open)"""),
            
            
            ]
        return mrd.Section("PostSynapticMech_Exp2Syn",
            "Needs double-checking!",
            parameter_table,
            mrd.EquationBlock( *eqns )
        )


mf.SummariserLibrary.register_summariser( PostSynapticMech_Exp2Syn_Base, PostSynapticMech_Exp2Syn_BaseSummariser) 
