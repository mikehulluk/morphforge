#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from collections import defaultdict

class NeuronParameter():
    def __init__(self, parametername, parameterunit, initialvalue = None, parameterrange=None):
        self.parametername = parametername
        self.parameterunit = parameterunit
        self.parameterrange = parameterrange
        self.initialvalue = initialvalue
    
    def getUnitStr(self):
        if not self.parameterunit: return ""
        if self.parameterunit.startswith("("): return self.parameterunit
        return "(%s)"%self.parameterunit 
        
            
        
    def declarationString(self):
        unitStr = self.getUnitStr() # "(%s)"%self.parameterunit if self.parameterunit else "" 
        rangeStr = "<%1.1e,%1.1e>"%self.parameterrange if self.parameterrange else ""
        return "%s %s %s"%(self.parametername,unitStr,rangeStr)
    
    def initialisationString(self ):
        #unitStr =  "(%s)"%self.parameterunit if self.parameterunit else ""
        unitStr = self.getUnitStr() #
        initStr = "= %s "%self.initialvalue if self.initialvalue else ""
        return  "%s %s %s"%(self.parametername,initStr, unitStr)
        



class ModFileSectioned(object):
    
    class Sections():
        Header = "HEADER" 
        Units = "UNITS"
        Neuron = "NEURON"
        Parameter = "PARAMETER"
        State = "STATE"
        Assigned = "ASSIGNED"
        Breakpoint = "BREAKPOINT"
        Initial = "INITIAL"
        Derivative = "DERIVATIVE"
        Functions = "FUNCTIONS"

        ordered = [ Header, Units, Neuron,  Parameter,  State,  Assigned,  Breakpoint, Initial,  Derivative,   Functions ]
        

    def __init__(self, title, comment=None):
        self.sectiondata = defaultdict(list)
        self.initialise()
        
        self.CreateHeader(title, comment)
        
    def prependToSection(self, section, line):
        self.sectiondata[section].insert(0,line)
    
    def appendToSection(self, section, line):
        self.sectiondata[section].append(line)
    
    def clearSection(self, section, line):
        del self.sectiondata[section]
    
    
    
    def getSectionText(self,section):
        return "\n".join(self.sectiondata[section])
    
    def getText(self):
        self.finalise()
        headered = [ self.getSectionText(section) for section in ModFileSectioned.Sections.ordered]
        return "\n\n".join(headered)
    
    
    
    
    # Initialisation
    def initialise(self):
        self.appendToSection( ModFileSectioned.Sections.Neuron, "THREADSAFE") 
    
    
    # Finalisation:
    def simpleFinaliseSection(self, section, tabsection=False):
        if tabsection: self.sectiondata[section] = [ "\t" + l for l in self.sectiondata[section] ] 
        self.prependToSection( section, "%s {"%section )
        self.appendToSection( section, "}" )
        
        
    def finalise(self):
        # Nothing to do for Header 
        self.simpleFinaliseSection( ModFileSectioned.Sections.Units, tabsection=True )
        self.simpleFinaliseSection( ModFileSectioned.Sections.Neuron, tabsection = True )
        self.simpleFinaliseSection( ModFileSectioned.Sections.Parameter, tabsection = True )
        self.simpleFinaliseSection( ModFileSectioned.Sections.State, tabsection = True )
        self.simpleFinaliseSection( ModFileSectioned.Sections.Assigned, tabsection = True )
        self.simpleFinaliseSection( ModFileSectioned.Sections.Breakpoint, tabsection = True )
        self.simpleFinaliseSection( ModFileSectioned.Sections.Initial, tabsection = True )
        
        #self.simpleFinaliseSection( ModFileSectioned.Sections.Derivative )
        
        
        # Nothing to do for Procedure
        # Nothing to do for Functions
        
    
    
    
    
    
    # User Functions:
    def CreateHeader(self, title, comment ):
        self.appendToSection( ModFileSectioned.Sections.Header, "TITLE %s"%title)
        self.appendToSection( ModFileSectioned.Sections.Header, "COMMENT")
        if comment: self.appendToSection( ModFileSectioned.Sections.Header, comment )
        self.appendToSection( ModFileSectioned.Sections.Header, "ENDCOMMENT")
    
    def AddUnitDefinition(self, unitname, unitsymbol):
        symbolStr = "%s"%unitsymbol if unitsymbol.startswith("(") else "(%s)"%unitsymbol
        nameStr = "%s"%unitname if unitname.startswith("(") else "(%s)"%unitname
        self.appendToSection( ModFileSectioned.Sections.Units, "%s = %s"%(symbolStr,nameStr) )
        
    
    def CreateNeuronInterface(self, suffix, ranges, nonspecificcurrents, ioncurrents=None, ):
        assert ioncurrents == None
        self.appendToSection( ModFileSectioned.Sections.Neuron, "SUFFIX %s"%suffix)
        
        self.appendToSection( ModFileSectioned.Sections.Neuron, "RANGE %s"% ",".join(ranges) )
        
        for current in nonspecificcurrents:
            self.appendToSection( ModFileSectioned.Sections.Neuron, "NONSPECIFIC_CURRENT %s"%current)
    
    def AddParameter(self, parameter):
        self.appendToSection( ModFileSectioned.Sections.Parameter, parameter.initialisationString() )
    
   
   
    # States
    def AddStateGroup( self, groupName, states, derivative_code, initial_code ):
        
        # Initial Block:
        self.appendToSection( ModFileSectioned.Sections.Initial, "\n".join(initial_code) )
        
        # Derivative Block:       
        derBlock = """DERIVATIVE %s{
        %s
        } """%( groupName, "\n".join( ["\t"+l for l in derivative_code] ))
        self.prependToSection( ModFileSectioned.Sections.Derivative, derBlock )
        
        #BreakPoint:
        solveStatement = "SOLVE %s METHOD cnexp"% groupName
        self.prependToSection( ModFileSectioned.Sections.Breakpoint,  solveStatement)
        
        #States Block:
        for state in states:
            self.appendToSection( ModFileSectioned.Sections.State, state.initialisationString() )    
        
        
    
    def AddAssigned(self, assigned):
        self.appendToSection( ModFileSectioned.Sections.Assigned, assigned.declarationString() )    
    
    def AddBreakPoint(self, equation):
        self.appendToSection( ModFileSectioned.Sections.Breakpoint, equation )
    
    def AddFunction(self, func):
        self.appendToSection( ModFileSectioned.Sections.Functions, func )
    
    
    
    
