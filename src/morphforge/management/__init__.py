
#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

from morphforge.simulation.neuron import NeuronSimulationEnvironment
from morphforge.simulationanalysis.summaries_new import SummariserLibrary



try:
    import mredoc as mrd
except ImportError:
    print 'Unable to import mredoc, you will be unable to produce pdf/html summaries'




def empty_str_matrix(N, M):
    return [ ['' for m in range(M)] for n in range(N) ]

def to_symbol(mech, env):
    return 'X' if mech in env else '-'


class PluginMgr(object):

    _environments = [NeuronSimulationEnvironment]



    @classmethod
    def _get_all_from_envs(cls, extract_functor):
        objs = []
        for env in cls._environments:
            objs.extend(extract_functor(env))
        return sorted(objs, key=lambda m: m.__name__)

    @classmethod
    def get_all_chls(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.membranemechanisms.keys() )

    @classmethod
    def get_all_iclamps(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.currentclamps.keys() )

    @classmethod
    def get_all_vclamps(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.voltageclamps.keys() )
    @classmethod
    def get_all_presynmechs(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.presynapticmechanisms.keys() )

    @classmethod
    def get_all_postsynmechs(cls):
        return cls._get_all_from_envs(
                extract_functor=lambda env:env.postsynapticmechanisms.keys() )





    @classmethod
    def summarise_all(cls):
        return mrd.SectionNewPage('Morphforge Configuration',
                cls.summarise_channels(),
                cls.summarise_currentclamps(),
                cls.summarise_voltageclamps(),
                cls.summarise_presynapticmechs(),
                cls.summarise_postsynapticmechs(),
                cls.summarise_tracemethods(),
                )


    @classmethod
    def summarise_channels(cls):
        mech_types = cls.get_all_chls()
        col1 = ['Channel Name'] + [mech.__name__ for mech in mech_types]
        cols = [ [env._env_name] + [ to_symbol(mech, env.membranemechanisms) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] +  [to_symbol(mech,SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Channels', mrd.VerticalColTable(rows[0], rows[1:]) )

    @classmethod
    def summarise_currentclamps(cls):
        mech_types = cls.get_all_iclamps()
        col1 = ['Clamp Name'] + [mech.__name__ for mech in mech_types]
        cols = [ [env._env_name] + [ to_symbol(mech, env.currentclamps) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] +  [to_symbol(mech,SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Current Clamps', mrd.VerticalColTable(rows[0], rows[1:]) )

    @classmethod
    def summarise_voltageclamps(cls):
        mech_types = cls.get_all_vclamps()
        col1 = ['Clamp Name'] + [mech.__name__ for mech in mech_types]
        cols = [ [env._env_name] + [ to_symbol(mech, env.voltageclamps) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] +  [to_symbol(mech,SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Voltage Clamps', mrd.VerticalColTable(rows[0], rows[1:]) )

    @classmethod
    def summarise_presynapticmechs(cls):
        mech_types = cls.get_all_presynmechs()
        col1 = ['PreSynMech'] + [mech.__name__ for mech in mech_types]
        cols = [ [env._env_name] + [ to_symbol(mech, env.presynapticmechanisms) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] +  [to_symbol(mech,SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Presynaptic Mechanisms', mrd.VerticalColTable(rows[0], rows[1:]) )
        #return mrd.Section('PreSynapticMechanisms', mrd.Paragraph('asda') ) 

    @classmethod
    def summarise_postsynapticmechs(cls):
        mech_types = cls.get_all_postsynmechs()
        col1 = ['PostSynMech'] + [mech.__name__ for mech in mech_types]
        cols = [ [env._env_name] + [ to_symbol(mech, env.postsynapticmechanisms) for mech in mech_types] for env in cls._environments]
        col_ = ['Summary'] +  [to_symbol(mech,SummariserLibrary.summarisers) for mech in mech_types] 
        cols = [col1] + cols + [col_]
        rows = zip(*cols)
        return mrd.Section('Postsynaptic Mechanisms', mrd.VerticalColTable(rows[0], rows[1:]) )

    @classmethod
    def summarise_tracemethods(cls):
        return TraceLibSummariser.summarise_all()



from morphforge.traces import TraceFixedDT, TraceVariableDT, TracePiecewise
from morphforge.traces import  TraceOperatorCtrl
import operator


operators = (
    (operator.__add__, '+'),
    (operator.__sub__, '-'),
    (operator.__mul__, '*'),
    (operator.__div__, '/'),
        )

class TraceLibSummariser(object):

    _trace_types = [TraceFixedDT, TraceVariableDT, TracePiecewise]

    @classmethod
    def summarise_all(cls):
        return mrd.Section('Tracs', 
                cls.summarise_methods(), 
                cls.summarise_operators(), 
                mrd.Paragraph('asda') ) 

    @classmethod
    def summarise_methods(cls):

        types = cls._trace_types


        return mrd.Section('TraceMethods', mrd.Paragraph('asda') ) 


    @classmethod
    def _get_all_operator_types(cls):
        types = set()
        for (op, lhs_type, rhs_type) in TraceOperatorCtrl.trace_operators_all:
            types.add(lhs_type)
            types.add(rhs_type)
        return sorted(list(types), key=lambda obj:(obj not in cls._trace_types, obj.__name__) )


    @classmethod
    def summarise_operators(cls):

        all_types = cls._get_all_operator_types()
        trace_types = cls._trace_types
        d = empty_str_matrix(N=len(all_types)+1, M=len(all_types)+1)


        for (i, tp1) in enumerate(all_types):
            d[0][i+1] = tp1.__name__
            d[i+1][0] = tp1.__name__
            for (j, tp2) in enumerate(all_types):

                # Neither of the operand is a trace_type:
                if not tp1 in trace_types and not tp2 in trace_types:
                    d[i+1][j+1] = '==='
                    continue

                outstr = ''
                for (op, sym) in operators:
                    key = (op, tp1, tp2)
                    if key in TraceOperatorCtrl.trace_operators_all:
                        outstr += sym
                d[i+1][j+1] += outstr
                d[j+1][i+1] += outstr

        tbl = mrd.VerticalColTable(d[0],d[1:], caption='Operators')

        return mrd.Section('TraceOperators', tbl )
