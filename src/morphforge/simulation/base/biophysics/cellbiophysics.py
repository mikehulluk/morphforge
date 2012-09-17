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

from morphforge.simulation.base.biophysics.passiveproperties import PassiveProperty
from morphforge.simulation.base.biophysics.membranemechanismtargetters import PassiveTargeter_EverywhereDefault
from morphforge.core.misc import SeqUtils


# A type for holding a mechanism/passive, where it is applied, and how much where.

class _MechanismTargetApplicator(object):

    def __init__(self, mechanism, targetter, applicator):
        self.mechanism = mechanism
        self.targetter = targetter
        self.applicator = applicator


class _PassiveTargetApplicator(object):

    def __init__(self, passiveproperty, targetter, value):
        self.passiveproperty = passiveproperty
        self.targetter = targetter
        self.value = value


class CellBiophysics(object):

    def __init__(self):
        self.appliedmechanisms = []
        self.appliedpassives = []

        # Add default passive configuration:
        self.add_passive(
                passiveproperty=PassiveProperty.AxialResistance,
                targetter=PassiveTargeter_EverywhereDefault(),
                value=PassiveProperty.defaults[PassiveProperty.AxialResistance])
        self.add_passive(
                passiveproperty=PassiveProperty.SpecificCapacitance,
                targetter=PassiveTargeter_EverywhereDefault(),
                value=PassiveProperty.defaults[PassiveProperty.SpecificCapacitance])

    # Active Mechanisms:
    # ####################
    def add_mechanism(self, mechanism, targetter, applicator):
        # Ensure the applicator is connected to the mechanism
        applicator.set_target_mechanism(mechanism)

        mta = _MechanismTargetApplicator(mechanism=mechanism, targetter=targetter, applicator=applicator)
        self.appliedmechanisms.append(mta)

    def get_resolved_mtas_for_section(self, section):

        # All the mechanisms targetting a certain region:
        mechanisms_targetting_section = [mta for mta in self.appliedmechanisms if mta.targetter.does_target_section(section)]

        mechanism_ids = set([mta.mechanism.get_mechanism_id() for mta in mechanisms_targetting_section])

        res = []
        for mech_id in mechanism_ids:
            mechs_of_i_dn_section = [mta for mta in mechanisms_targetting_section if mta.mechanism.get_mechanism_id() == mech_id]
            highest_prority_mech = SeqUtils.max_with_unique_check(mechs_of_i_dn_section, key=lambda pta: pta.targetter.get_priority())
            res.append(highest_prority_mech)
        return res

    # Used for summariser:
    def get_applied_mtas(self):
        return self.appliedmechanisms

    def get_all_mechanisms_applied_to_cell(self):
        return set([mta.mechanism for mta in self.appliedmechanisms])


    def get_mechanism_ids(self):
		# TODO: REMOVE HERE!
        return set([mta.mechanism.get_mechanism_id() for mta in
                   self.appliedmechanisms])

    def get_mta_by_mechanism_id_for_section(self, mech_id, section):
        assert False, 'Deprecated? 2012-01-20'
        return SeqUtils.expect_single([mta for mta in self.get_resolved_mtas_for_section(section=section) if mta.mechanism.get_mechanism_id() == mech_id])

    def get_chl(self, chlname):
        return SeqUtils.filter_expect_single(self.get_all_mechanisms_applied_to_cell(), lambda mech: mech.name==chlname)






    # Passives:
    def add_passive(self, passiveproperty, targetter, value):
        pta = _PassiveTargetApplicator(passiveproperty=passiveproperty, targetter=targetter, value=value)
        self.appliedpassives.append(pta)

    def get_passives_for_section(self, section):

        sectionptas = [pta for pta in self.appliedpassives
                       if pta.targetter.does_target_section(section)]
        passivemechs = {}
        for passiveproperty in PassiveProperty.all:
            section_property_ptas = [spta for spta in sectionptas if spta.passiveproperty == passiveproperty]
            highest_prority_mech = SeqUtils.max_with_unique_check(section_property_ptas, key=lambda pta: pta.targetter.get_priority())
            passivemechs[passiveproperty] = highest_prority_mech
        return passivemechs

    def get_passive_property_for_section(self, section, passive):
        return self.get_passives_for_section(section)[passive].value



    # Used for summariser:
    def get_applied_passives(self):
        return self.appliedpassives



    # Used for summariser:
    def get_applied_mechanisms(self):
        assert False, 'should be using get_applied_mtas()'
        return self.appliedmechanisms


