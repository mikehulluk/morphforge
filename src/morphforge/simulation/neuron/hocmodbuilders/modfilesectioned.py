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


from collections import defaultdict

class NeuronParameter(object):
    def __init__(self, parametername, parameterunit, initialvalue=None, parameterrange=None):
        self.parametername = parametername
        self.parameterunit = parameterunit
        self.parameterrange = parameterrange
        self.initialvalue = initialvalue

    def get_unit_str(self):
        if not self.parameterunit:
            return ''
        if self.parameterunit.startswith('('):
            return self.parameterunit
        return '(%s)' % self.parameterunit



    def declaration_string(self):
        unit_str = self.get_unit_str() # "(%s)"%self.parameterunit if self.parameterunit else ""
        range_str = "<%1.1e,%1.1e>"%self.parameterrange if self.parameterrange else ""
        return "%s %s %s"%(self.parametername,unit_str,range_str)

    def initialisation_string(self):
        #unit_str =  "(%s)"%self.parameterunit if self.parameterunit else ""
        unit_str = self.get_unit_str() #
        init_str = "= %s "%self.initialvalue if self.initialvalue else ""
        return  "%s %s %s"%(self.parametername,init_str, unit_str)




class ModFileSectioned(object):

    class Sections(object):

        Header = 'HEADER'
        Units = 'UNITS'
        Neuron = 'NEURON'
        Parameter = 'PARAMETER'
        State = 'STATE'
        Assigned = 'ASSIGNED'
        Breakpoint = 'BREAKPOINT'
        Initial = 'INITIAL'
        Derivative = 'DERIVATIVE'
        Functions = 'FUNCTIONS'

        ordered = [
            Header,
            Units,
            Neuron,
            Parameter,
            State,
            Assigned,
            Breakpoint,
            Initial,
            Derivative,
            Functions,
           ]

    def __init__(self, title, comment=None):
        self.sectiondata = defaultdict(list)
        self.initialise()

        self.create_header(title, comment)

    def prepend_to_section(self, section, line):
        self.sectiondata[section].insert(0, line)

    def append_to_section(self, section, line):
        self.sectiondata[section].append(line)

    def clear_section(self, section, line):
        del self.sectiondata[section]



    def get_section_text(self, section):
        return '\n'.join(self.sectiondata[section])

    def get_text(self):
        self.finalise()
        headered = [self.get_section_text(section) for section in ModFileSectioned.Sections.ordered]
        return "\n\n".join(headered)




    # Initialisation
    def initialise(self):
        self.append_to_section(ModFileSectioned.Sections.Neuron,
                               'THREADSAFE')


    # Finalisation:
    def simple_finalise_section(self, section, tabsection=False):
        if tabsection: self.sectiondata[section] = ["\t" + l for l in self.sectiondata[section]]
        self.prepend_to_section(section, "%s {"%section)
        self.append_to_section(section, "}")


    def finalise(self):
        # Nothing to do for Header
        self.simple_finalise_section(ModFileSectioned.Sections.Units, tabsection=True)
        self.simple_finalise_section(ModFileSectioned.Sections.Neuron, tabsection = True)
        self.simple_finalise_section(ModFileSectioned.Sections.Parameter, tabsection = True)
        self.simple_finalise_section(ModFileSectioned.Sections.State, tabsection = True)
        self.simple_finalise_section(ModFileSectioned.Sections.Assigned, tabsection = True)
        self.simple_finalise_section(ModFileSectioned.Sections.Breakpoint, tabsection = True)
        self.simple_finalise_section(ModFileSectioned.Sections.Initial, tabsection = True)

        # Nothing to do for Procedure
        # Nothing to do for Functions






    # User Functions:
    def create_header(self, title, comment):
        self.append_to_section(ModFileSectioned.Sections.Header, "TITLE %s" % title)
        self.append_to_section(ModFileSectioned.Sections.Header, "COMMENT")
        if comment: self.append_to_section(ModFileSectioned.Sections.Header, comment)
        self.append_to_section(ModFileSectioned.Sections.Header, "ENDCOMMENT")

    def add_unit_definition(self, unitname, unitsymbol):
        symbol_str = "%s" % unitsymbol if unitsymbol.startswith("(") else "(%s)"%unitsymbol
        name_str = "%s" % unitname if unitname.startswith("(") else "(%s)"%unitname
        self.append_to_section(ModFileSectioned.Sections.Units, "%s = %s"%(symbol_str,name_str))


    def create_neuron_interface(self, suffix, ranges, nonspecificcurrents, ioncurrents=None,):
        assert ioncurrents == None
        self.append_to_section(ModFileSectioned.Sections.Neuron,
                               'SUFFIX %s' % suffix)

        self.append_to_section(ModFileSectioned.Sections.Neuron,
                               'RANGE %s' % ','.join(ranges))

        for current in nonspecificcurrents:
            self.append_to_section(ModFileSectioned.Sections.Neuron,
                                   'NONSPECIFIC_CURRENT %s' % current)

    def add_parameter(self, parameter):
        self.append_to_section(ModFileSectioned.Sections.Parameter,
                               parameter.initialisation_string())



    # States
    def add_state_group(self, groupname, states, derivative_code, initial_code):

        # Initial Block:
        self.append_to_section(ModFileSectioned.Sections.Initial, "\n".join(initial_code))

        # Derivative Block:
        der_block = """DERIVATIVE %s{
        %s
        } """%(groupname, "\n".join(["\t"+l for l in derivative_code]))
        self.prepend_to_section(ModFileSectioned.Sections.Derivative, der_block)

        #BreakPoint:
        solve_statement = "SOLVE %s METHOD cnexp"% groupname
        self.prepend_to_section(ModFileSectioned.Sections.Breakpoint,  solve_statement)

        #States Block:
        for state in states:
            self.append_to_section(ModFileSectioned.Sections.State, state.initialisation_string())



    def add_assigned(self, assigned):
        self.append_to_section(ModFileSectioned.Sections.Assigned,
                               assigned.declaration_string())

    def add_breakpoint(self, equation):
        self.append_to_section(ModFileSectioned.Sections.Breakpoint,
                               equation)

    def add_function(self, func):
        self.append_to_section(ModFileSectioned.Sections.Functions,
                               func)




