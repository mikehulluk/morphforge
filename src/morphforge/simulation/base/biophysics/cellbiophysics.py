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

import types
from morphforge.core import SeqUtils

from morphforge.simulation.base.biophysics.passiveproperties import PassiveProperty
from morphforge.simulation.base.biophysics.channeltargetters import PassiveTargetterEverywhereDefault
from morphforge.simulation.base.biophysics.channelapplicators import ChannelApplicatorUniform
from morphforge.simulation.base.biophysics.channeltargetters import ChannelTargeterEverywhere
from morphforge.simulation.base.biophysics.channeltargetters import ChannelTargeterRegion
from morphforge.simulation.base.biophysics.channeltargetters import PassiveTargetterEverywhere



# A type for holding a channel/passive, where it is applied, and how much where.

class _MechanismTargetApplicator(object):

    def __init__(self, channel, targetter, applicator):
        self.channel = channel
        self.targetter = targetter
        self.applicator = applicator


class _PassiveTargetApplicator(object):

    def __init__(self, passiveproperty, targetter, value):
        self.passiveproperty = passiveproperty
        self.targetter = targetter
        self.value = value


class CellBiophysics(object):

    def __init__(self, cell):
        self._cell = cell
        self.appliedmechanisms = []
        self.appliedpassives = []

        # Add default passive configuration:
        self.add_passive(
                passiveproperty=PassiveProperty.AxialResistance,
                targetter=PassiveTargetterEverywhereDefault(),
                value=PassiveProperty.defaults[PassiveProperty.AxialResistance])
        self.add_passive(
                passiveproperty=PassiveProperty.SpecificCapacitance,
                targetter=PassiveTargetterEverywhereDefault(),
                value=PassiveProperty.defaults[PassiveProperty.SpecificCapacitance])

    # Active Channels:
    # ####################
    def add_channel(self, channel, targetter, applicator):
        # Ensure the applicator is connected to the channel
        applicator.set_target_channel(channel)

        mta = _MechanismTargetApplicator(channel=channel, targetter=targetter, applicator=applicator)
        self.appliedmechanisms.append(mta)

    def get_resolved_mtas_for_section(self, section):

        # TODO: Some basic error checking here: we should ensure that if we specialise a region/section, then we also
        # cover the Everywhere. This should help us catch errors in ehich the user creates 2 mechanisms of the same thing, and 
        # and so applies the same channel twice accidentally.

        # All the mechanisms targetting a certain region:
        mtas_targetting_section = [mta for mta in self.appliedmechanisms if mta.targetter.does_target_section(section)]
        channels_targetting_section = set([ mta.channel for mta in mtas_targetting_section])

        resolved_chls = []
        for chl in channels_targetting_section:
            mtas_with_chl = [mta for mta in mtas_targetting_section if mta.channel is chl]
            highest_prority_chl = SeqUtils.max_with_unique_check(mtas_with_chl, key=lambda pta: pta.targetter.get_priority())
            resolved_chls.append(highest_prority_chl)
        return resolved_chls


    # Used for summariser:
    def get_applied_mtas(self):
        return self.appliedmechanisms

    def get_all_channels_applied_to_cell(self):
        return set([mta.channel for mta in self.appliedmechanisms])

    #def get_channels(self):
    #    # TODO: RENAME ONE OF THESE!
    #    return self.get_all_channels_applied_to_cell()

    def get_channel(self, name):
        try:
            return SeqUtils.filter_expect_single(self.get_all_channels_applied_to_cell(), lambda chl: chl.name==name)
        except:
            print 'Options: ', [ chl.name for chl in self.get_all_channels_applied_to_cell() ]
            raise



    # Simplified interface to adding channels:
    def apply_channel(self, channel, where = None, parameter_overrides=None, parameter_multipliers=None):
        """ A simplified interface to applying channels.  """

        from morphforge.morphology.core import Region

        # Resolve 'where' if its a string:
        if isinstance(where, basestring):
            morphology = self._cell.morphology
            assert not (where in morphology.get_region_names() and where in morphology.get_idtags()), 'where ambigious: %s'%where
            if where in morphology.get_region_names():
                where = morphology.get_region(name=where)
            elif where in morphology.get_idtags():
                raise NotImplementedError()
            else:
                assert False, 'I dont knwo what to do with: %s' % where

        # Convert where to a targetter:
        where_to_targetter_LUT = {
                types.NoneType: lambda: ChannelTargeterEverywhere(),
                Region: lambda: ChannelTargeterRegion(where)
        }

        # Build targetters and applicators:
        targetter = where_to_targetter_LUT[type(where)]()
        applicator=ChannelApplicatorUniform( parameter_multipliers=parameter_multipliers, parameter_overrides=parameter_overrides)

        return self.add_channel(
            channel=channel,
            targetter=targetter,
            applicator=applicator
            )





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




    def set_passive(self, passiveproperty, value, where=None,):
        assert passiveproperty in PassiveProperty.all
        if where != None:
            raise NotImplementedError()
        self.add_passive(passiveproperty=passiveproperty,
                         targetter=PassiveTargetterEverywhere(),
                         value=value)

