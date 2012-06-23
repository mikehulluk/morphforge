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


from morphforgecontrib.simulation.membranemechanisms import inftauinterpolated
from morphforgecontrib.simulation.default.core.mmalphabeta import MM_AlphaBetaChannel
from morphforgecontrib.simulation.default.core.mmalphabetabeta import MM_AlphaBetaBetaChannel
from numpy.core.function_base import linspace
from morphforgecontrib.simulation.membranemechanisms.inftauinterpolated.core import MM_InfTauInterpolatedChannel,\
    InfTauInterpolation
from morphforgecontrib.simulation.default.summarisers.util import InfTauCalculator
from morphforge.core.quantities.fromcore import unit
import quantities as pq



class ChannelConverter(object):


    @classmethod
    def AlphaBetaToInterpolateInfTauFunctorConvertor(cls, chl_functor, new_id=None, new_name=None, clone_id_suffix="_AsInfTau",clone_name_suffix="_AsInfTau", voltage_interpolation_values=None,   ):


        # Create a new functor:
        def newFunctor( env, _voltage_interpolation_values=voltage_interpolation_values):

            #print V


            old_chl = chl_functor(env)
            assert isinstance(old_chl, (MM_AlphaBetaChannel,MM_AlphaBetaBetaChannel)) #or issubclass(MM_AlphaBetaBetaChannel, old_chl)

            # New ID:
            if new_id is not None:
                chl_id = new_id
            else:
                chl_id = old_chl.mechanism_id + clone_id_suffix

            # New Name
            if new_name is not None:
                chl_name = new_name
            else:
                chl_name = old_chl.mechanism_id + clone_name_suffix


            # Interpolation voltages:
            #voltage_interpolation_values=voltage_interpolation_values
            if _voltage_interpolation_values is None:
                _voltage_interpolation_values = linspace(-80,60,10) * unit('mV')

                        # Copy the state variables
            new_state_vars = {}
            for state_var in old_chl.get_state_variables():
                alpha,beta = old_chl.get_alpha_beta_at_voltage(statevar=state_var, V=_voltage_interpolation_values)
                inf, tau = InfTauCalculator.alpha_beta_to_inf_tau(alpha,beta)
                V =   _voltage_interpolation_values.rescale('mV').magnitude
                inf = inf.rescale(pq.dimensionless).magnitude
                tau = tau.rescale('ms').magnitude
                new_state_vars[state_var] = InfTauInterpolation(V=V, inf=inf, tau=tau)




            mech = env.MembraneMechanism( MM_InfTauInterpolatedChannel,
                                   name=chl_name,
                                   mechanism_id=chl_id,
                                   ion=old_chl.ion,
                                   equation=old_chl.eqn,
                                   conductance = old_chl.conductance,
                                   reversalpotential = old_chl.reversalpotential,
                                   statevars_new = new_state_vars )
            return mech

        return newFunctor

#        V1 = self.state1.plotinf.lineplot.index.get_data().tolist()
#        inf1 = self.state1.plotinf.lineplot.value.get_data().tolist()
#        tau1 = self.state1.plottau.lineplot.value.get_data().tolist()
#
#        V2 = self.state2.plotinf.lineplot.index.get_data().tolist()
#        inf2 = self.state2.plotinf.lineplot.value.get_data().tolist()
#        tau2 = self.state2.plottau.lineplot.value.get_data().tolist()
#
#        #V1 = self.state1.plotinf.mx.tolist()
#        #inf1 = self.state1.plotinf.my.tolist()
#        #tau1 = self.state1.plottau.my.tolist()
#        #V2 = self.state2.plotinf.mx.tolist()
#        #inf2 = self.state2.plotinf.my.tolist()
#        #tau2 = self.state2.plottau.my.tolist()
#
#        ks_vars = {
#                self.state_var_name1: InfTauInterpolation(V=V1, inf=inf1, tau=tau1),
#                self.state_var_name2: InfTauInterpolation(V=V2, inf=inf2, tau=tau2),
#                }
#
#        #inf_data1 = zip( self.state1.plotinf.mx.tolist(), self.state1.plotinf.my.tolist() )
#        #tau_data1 = zip( self.state1.plottau.mx.tolist(), self.state1.plottau.my.tolist() )
#
#        #inf_data2 = zip( self.state2.plotinf.mx.tolist(), self.state2.plotinf.my.tolist() )
#        #tau_data2 = zip( self.state2.plottau.mx.tolist(), self.state2.plottau.my.tolist() )
#        #
#        #ks_vars = {
#        #        self.state_var_name1: { 'inf': inf_data1, 'tau': tau_data1, },
#        #        self.state_var_name2: { 'inf': inf_data2, 'tau': tau_data2, },
#        #
#        #        }
#        ks = env.MembraneMechanism( MM_InfTauInterpolatedChannel,
#                                      name=self.chlname,
#                                      ion='None',
#                                      equation=self.eqn,
#                                      mechanism_id=self.mechanism_id,
#                                      conductance = '%2.2f:mS/cm2'%gbar,
#                                      reversalpotential = '%2.2f:mV'%vrev,
#                                      statevars_new = ks_vars )
#
#
#
#
#                caStateVars = { "m": {"alpha": [4.05,0.0,1.0,-15.32,-13.57], "beta1": [0.093 * 10.63, 0.093,-1,10.63, 1], "beta2":[1.28,0,1,5.39,12.11] } }
#    caChannels = env.MembraneMechanism(
#                            MM_CalciumAlphaBetaBetaChannel,
#                            name="CaChl", ion="ca",
#                            equation="m*m",
#                            permeability = unit("1.425:cm/s") * 0.1 * 0.15,
#                            intracellular_concentration = unit("100:nMol"),
#                            extracellular_concentration = unit("10:uMol"),
#                            temperature = unit("300:K"),
#                            beta2threshold = unit("-25:mV"),
#                            statevars=caStateVars,
#                            mechanism_id = 'HULL12_RB_CA_ID'
#                            )
#    return caChannels
#
#
#
#
#
#
#            state_names = chl.statevars.keys()
#            assert len(state_names) == 2
#            state_name1 = state_names[0]
#            state_name2 = state_names[1]
#
#            [intV,tauV],[intV,infV] = convertAlphaBetaToInfTauInterpolated( chl, state_name1, 10)
#            state1=HHGeneralStatePanel(initial_tau= [intV,tauV], initial_inf=[intV,infV] )
#
#            [intV,tauV],[intV,infV] = convertAlphaBetaToInfTauInterpolated( chl, state_name2, 10)
#            state2=HHGeneralStatePanel(initial_tau= [intV,tauV], initial_inf=[intV,infV] )
#
#            return HHChannelPaneInfTau2( sim_config=sim_config,
#                                         general_pane=general,
#                                         state_pane1=state1,
#                                         state_pane2=state2,
#                                         eqn = chl.eqn,
#                                         mechanism_id = chl.mechanism_id,
#                                         state_var_name1 = state_name1,
#                                         state_var_name2 = state_name2,
#                                         chlname = chlname
#                                        )
#


