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
from morphforge.core import getStringMD5Checksum

def getMD5OfRegion(r):
    #assert False # Is this Cruft?? Added Jan 2011
    return getStringMD5Checksum(r.name)

def getMD5OfSection(s):
    #assert False # Is this Cruft?? Added Jan 2011
    sectionString = " %2.2f %2.2f %2.2f %2.2f "
    regionsString = getMD5OfRegion(s.region) if s.region else ""
    childrenString = ",".join( [getMD5OfSection(s) for s in s.children] )
    idString = "" if not s.idTag else getStringMD5Checksum(s.idTag)
    
    return getStringMD5Checksum( sectionString + regionsString + childrenString + idString)


def getMD5OfMorphology(m):
    #assert False # Is this Cruft?? Added Jan 2011
    treemd5 = getMD5OfSection(m._dummysection)
    nameMD5 = getStringMD5Checksum(m.name)
    assert not m.metadata
    regionsMD5 = ",".join( [ getMD5OfRegion(r) for r in m.getRegions() ])
    return getStringMD5Checksum(treemd5 + nameMD5 + regionsMD5)


