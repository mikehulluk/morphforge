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


class StandardTags(object):

    # Its important the spellings are the same;
    # since we use the values in setattr() to automatically populate classes.

    Voltage = "Voltage"
    CurrentDensity = "CurrentDensity"
    Current = "Current"
    Conductance = "Conductance"
    ConductanceDensity = "ConductanceDensity"

    StateVariable = "StateVariable"
    StateTimeConstant = "StateTimeConstant"
    StateSteadyState = "StateSteadyState"

    NMDAVoltageDependancy = "NMDAVoltageDependancy"
    NMDAVoltageDependancySS = "NMDAVoltageDependancySS"

    Event = "Event"

    DefaultUnits = {
                    Voltage: "mV",
                    CurrentDensity: "mA/cm2",
                    Current: "pA",
                    ConductanceDensity: "mS/cm2",
                    Conductance: "pS",
                    StateVariable: "",
                    StateTimeConstant: "ms",
                    StateSteadyState: "",
                    NMDAVoltageDependancy:"",
                    NMDAVoltageDependancySS:"",

                    }

    label = {
                    Voltage: "Voltage",
                    CurrentDensity: "Current Density",
                    Current: "Current",
                    ConductanceDensity: "Conductance Density",
                    Conductance: "Conductance",
                    StateVariable: "State Variable",
                    StateTimeConstant: "StateVariable Time Constant",
                    StateSteadyState: "StateVariable Steddy State",
                    NMDAVoltageDependancy: "NMDA Voltage Dependancy",
                    NMDAVoltageDependancySS: "NMDA Voltage Dependancy Steady State",
                    }

