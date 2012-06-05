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
class TagSelector(object):
    def __call__(self, tr):
        raise NotImplementedError()

    @classmethod
    def fromString(cls, s):
        from tagselectorstringparser import parseString
        return parseString(s, )

    # Operator Overloading:
    def __and__(self, rhs):
        assert isinstance(rhs, TagSelector)
        return TagSelectorAnd(lhs=self, rhs=rhs)

    def __or__(self, rhs):
        assert isinstance(rhs, TagSelector)
        return TagSelectorOr(lhs=self, rhs=rhs)

    def select(self, trs):
        return [tr for tr in trs if self(tr)]



class TagSelectorAny(TagSelector):
    def __init__(self,tags):
        self.tags = set( tags )

    def __call__(self,tr):
        return not set(self.tags).isdisjoint(tr.tags)


class TagSelectorAll(TagSelector):
    def __init__(self,tags):
        self.tags = set( tags )

    def __call__(self,tr):
        return self.tags.issubset( set( tr.tags) )




class TagSelectorBinary(TagSelector):
    def __init__(self, lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs

class TagSelectorOr(TagSelectorBinary):
    def __call__(self,tr):
        return self.lhs(tr) or self.rhs(tr)

class TagSelectorAnd(TagSelectorBinary):
    def __call__(self,tr):
        return self.lhs(tr) and self.rhs(tr)


class TagSelectorNot(TagSelector):
    def __init__(self, rhs):
        self.rhs = rhs
    def __call__(self, tr):
        return not self.rhs(tr)






class TagSelect(TagSelectorAll):
    def __init__(self, s):
        assert isinstance( s, basestring)
        TagSelectorAll.__init__(self, tags=[s])



