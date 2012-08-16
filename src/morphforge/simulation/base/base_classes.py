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


from morphforge.core import ObjectLabeller

class NamedSimulationObject(object):
    
    """ A base class for any object in a simulation that needs a name.

    This class ensures that no two objects in a simulation have the same
    name.
    """

    """ A dictionary -> set mapping, recording what object names are in 
    use at all simulations"""
    
    _obj_names = {}


    def __init__(self, simulation, name=None):


        assert simulation is not None

        if not simulation in NamedSimulationObject._obj_names:
            NamedSimulationObject._obj_names[simulation] = set()

        if not name:
            name = ObjectLabeller.get_next_unamed_object_name(
                    obj_type=NamedSimulationObject,
                    prefix='AnonObj')

        assert not name in NamedSimulationObject._obj_names[simulation]
        NamedSimulationObject._obj_names[simulation].add(name)

        self._name = name
        self._simulation = simulation

    def get_name(self):
        return self._name

    name = property(get_name)

    @property
    def simulation(self):
        return self._simulation

