#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
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
from morphforge.core import CheckValidName

class Region(object):
    """
    Region is a collection of sections. It is used for annotating the sections
    (i.e. axon, soma, proximal dendrite, ...) and for collectively assigning 
    the channels and membrane definitions to the sections.
    """    
    
    
    def __str__(self):
        s = "<RegionObject: Name: %s, nSections: %d>" % (self.name, len(self.sections) )
        return s
    def __init__(self, name):
        CheckValidName(name)
        self.name = name
        self.sections = []
        self.morph = None
    
    
    def __iter__(self):
        return iter(self.sections)
    
    def addSection(self, section):
        """Adding a section to the region."""
        
        if section in self.sections: 
            raise ValueError("Section already in Region.sections")

        self.sections.append(section)
        
    
    def setMorph(self, morph):

        if not morph: 
            raise ValueError()
        if self.morph: 
            raise ValueError()
        self.morph = morph
