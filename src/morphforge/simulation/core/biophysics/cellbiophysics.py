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
import collections
from morphforge.simulation.core.biophysics.passiveproperties import PassiveProperty
from morphforge.simulation.core.biophysics.membranemechanismtargetters import PassiveTargeter_EverywhereDefault


# A type for holding a mechanism/passive, where it is applied, and how much where.

MechanismTargetApplicator = collections.namedtuple('MechanismTargetApplicator', ['mechanism', 'targetter', 'applicator'],)
PassiveTargetApplicator = collections.namedtuple('PassiveTargetApplicator', ['passiveproperty', 'targetter', 'value'],)

from morphforge.core.misc import SeqUtils

class CellBiophysics(object):
  
    def __init__(self):     
        #tuples of (mechanism, targeter,applicator,mechanism)
        self.appliedmechanisms = [] 
        self.appliedpassives = []
      
        self.addPassive(
             passiveproperty = PassiveProperty.AxialResistance, 
             targetter = PassiveTargeter_EverywhereDefault(), 
             value = PassiveProperty.defaults[PassiveProperty.AxialResistance] )
        
        self.addPassive(
             passiveproperty = PassiveProperty.SpecificCapacitance, 
             targetter = PassiveTargeter_EverywhereDefault(), 
             value =  PassiveProperty.defaults[PassiveProperty.SpecificCapacitance] )
      
    # Active Mechanisms:
    # ####################
    def addMechanism(self, mechanism, targetter, applicator):
        mta = MechanismTargetApplicator(mechanism=mechanism, targetter=targetter, applicator=applicator)
        self.appliedmechanisms.append(mta) 
      
    def getResolvedMTAsForSection(self, section):
        
        # All the mechanisms targetting a certain region:
        mechanismsTargettingSection = [ mta for mta in self.appliedmechanisms if mta.targetter.doesTargetSection(section) ]
        
        mechanismIDs = set([ mta.mechanism.getMechanismID() for mta in mechanismsTargettingSection])
        
        res = []
        for mechID in mechanismIDs:
            mechsOfIDnSection = [mta for mta in mechanismsTargettingSection if mta.mechanism.getMechanismID() == mechID]            
            highestProrityMech = SeqUtils.max_with_unique_check( mechsOfIDnSection, key=lambda pta: pta.targetter.getPriority() )  
            res.append( highestProrityMech )
        return res 
    
    # Used for summariser:
    def getAppliedMTAs(self):
        return self.appliedmechanisms
    
    
    #def getAppliedMechanisms_mechanism(self):
    #    ms = [ mta.mechanism for mta in self.appliedmechanisms ]
    #    return set(ms)
    
    
    def getAllMechanismsAppliedToCell(self):
        ms = [ mta.mechanism for mta in self.appliedmechanisms ]
        return set(ms)
    
    
    def getMechanismIDs(self):
        return set( [mta.mechanism.getMechanismID() for mta in self.appliedmechanisms] )
    
    def getMTAByMechanismIDForSection(self, id, section):
        assert False,'Deprecated? 2012-01-20'
        return SeqUtils.expect_single( [ mta for mta in self.getResolvedMTAsForSection(section=section) if mta.mechanism.getMechanismID()==id ] )
    
    
    
    
    
    
    # Passives:
    def addPassive(self, passiveproperty, targetter, value):
        pta = PassiveTargetApplicator(passiveproperty=passiveproperty, targetter=targetter, value=value)
        self.appliedpassives.append(pta) 
    
 
    def getPassivesForSection(self, section):
        
        sectionptas = [ pta for pta in self.appliedpassives if  pta.targetter.doesTargetSection(section) ]
        passivemechs = {}
        for passiveproperty in PassiveProperty.all:
            section_property_ptas = [ spta for spta in sectionptas if spta.passiveproperty == passiveproperty ]
            highestProrityMech = SeqUtils.max_with_unique_check( section_property_ptas, key=lambda pta: pta.targetter.getPriority() )  
            passivemechs[passiveproperty] =  highestProrityMech
        return passivemechs
            
    def getPassivePropertyForSection(self, section, passive  ):
        return self.getPassivesForSection(section)[passive].value
        

     
    # Used for summariser:
    def getAppliedMechanisms(self):
        assert False, "should be using getAppliedMTAs()"
        return self.appliedmechanisms
    
    



    
