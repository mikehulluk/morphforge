#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
""" Visitor Base Classes: Here be Dragons!"""

#import numpy

#from morphforge.core import ExactlyOneNotNone
from morphforge.core import SeqUtils






class SectionVisitorDF(object):


    #@classmethod
    #def build(cls, functor, morph ):
    #    v = SectionVisitorDF(functor=functor)
    #    return v(morph)


    def __init__(self, functor, morph=None, dummysectionfunctor=None, rootsectionfunctor=None, returnfunctor=lambda:None, pretraversefunctor=lambda:None, posttraversefunctor=lambda:None):
        self.functor = functor
        self.dummysectionfunctor = dummysectionfunctor
        self.rootsectionfunctor = rootsectionfunctor if rootsectionfunctor else functor
        self.returnfunctor = returnfunctor
        self.pretraversefunctor = pretraversefunctor
        self.posttraversefunctor = posttraversefunctor

        self.alreadycalled = False
        self.morph = morph

        if self.morph != None:
            self.__call__()

    def __call__(self, morph=None):
        #self.morph = ExactlyOneNotNone(morph, self.morph)
        self.morph = SeqUtils.filter_expect_single(
                        [morph, self.morph], lambda s: s is not None)
        if not self.alreadycalled:
            self.pretraversefunctor()
            self.visit_section_internal(self.morph.get_dummy_section())
            self.posttraversefunctor()
            self.alreadycalled = True

        return self.returnfunctor()

    def is_visit_root(self):
        return self.rootsectionfunctor != None

    def is_visit_dummy(self):
        return self.dummysectionfunctor != None


    def visit_section_internal(self, section):
        """ Implements:  1. visit the node. 2. Traverse the subtrees. """
        if section.is_dummy_section():
            if self.is_visit_dummy():
                #assert False
                assert False, 'Should not get here, refactoring starting Jun-12'
            #if self.is_visit_dummy():
            #    assert False
            #    self.dummysectionfunctor(section)
        elif section.is_a_root_section():
            if self.is_visit_root():
                self.rootsectionfunctor(section)
        else:
            self.functor(section)

        for c in section.children:
            self.visit_section_internal(c)








class SectionVisitorDFOverrider(SectionVisitorDF):

    def __init__(self, **kwargs):
        super(SectionVisitorDFOverrider, self).__init__(functor=self.visit_section, rootsectionfunctor=self.visit_root_section, **kwargs )

    def visit_section(self, section):
        raise NotImplementedError()

    def visit_root_section(self, section):
        raise NotImplementedError()




class SectionVisitorHomogenousOverrider(SectionVisitorDFOverrider):

    def __init__(self, functor, section_result_operator=None, **kwargs):
        self.section_result_operator = section_result_operator
        self.myfunctor = functor
        super(SectionVisitorHomogenousOverrider, self).__init__( **kwargs )

    def visit_section(self, section):
        res =  self.myfunctor( section )
        if self.section_result_operator:
            self.section_result_operator(section,res)
        return res

    def visit_root_section(self, section):
        return self.visit_section(section)





class DictBuilderSectionVisitorHomo(SectionVisitorHomogenousOverrider):
    def __init__(self,  functor, morph=None):
        self.dict = {}
        super(DictBuilderSectionVisitorHomo, self).__init__(section_result_operator=self.add_to_dict, functor=functor, returnfunctor=lambda:self.dict, morph=morph )

    def add_to_dict(self,section,result):
        self.dict[section] = result




class ListBuilderSectionVisitor(SectionVisitorDF):
    def __init__(self, functor, rootfunctor=None, morph=None):
        self.sectFunctor = functor
        self.sectRootFunctor = rootfunctor if rootfunctor else functor
        self.list = []

        super(ListBuilderSectionVisitor, self).__init__(morph=morph, functor=self.visit_section, rootsectionfunctor=self.visit_root_section, returnfunctor=lambda:self.list)

    def visit_section(self, section):
        self.list.append(self.sectFunctor(section))

    def visit_root_section(self, section):
        if self.sectRootFunctor:
            self.list.append(self.sectRootFunctor(section))




#class NumpyBuilderSectionVisitor(SectionVisitorDF):
#    def __init__(self, functor, rootfunctor = None, morph=None, ndims=1, datatype=float):
#        self.sectFunctor = functor
#        self.sectRootFunctor = rootfunctor if rootfunctor else functor
#
#        self.array = None
#        self.sectionIndexer = None
#        self.ndims = ndims
#        self.datatype = datatype
#
#        super(NumpyBuilderSectionVisitor, self).__init__(morph=morph,
#                                                       functor=self.visit_section,
#                                                       rootsectionfunctor=self.visit_root_section,
#                                                       returnfunctor=lambda:self.array,
#                                                       pretraversefunctor=self.buildIndexerAndArray
#                                                       )
#
#
#    def buildIndexerAndArray(self):
#        self.sectionIndexer = SectionIndexerDF(self.morph)()
#        self.array = numpy.zeros((len(self.sectionIndexer), self.ndims,), self.datatype)
#
#
#    def visit_section(self, section):
#        self.array[ self.sectionIndexer[section] ] = self.sectFunctor(section)
#
#    def visit_root_section(self, section):
#        self.array[ self.sectionIndexer[section] ] = self.sectRootFunctor(section)




class SectionIndexerDF(DictBuilderSectionVisitorHomo):
    """Create a dictionary that maps section objects to sequential integers"""
    def __init__(self, morph=None,offset=0):
        functor = lambda s: len(self.dict) + offset
        super(SectionIndexerDF, self).__init__(morph=morph, functor=functor)



SectionIndexerWithOffsetDF = SectionIndexerDF
# I reckon this can probably be combined into the class above, but I have not tried it yet!
#class SectionIndexerWithOffsetDF(DictBuilderSectionVisitor):
#    pass
#    """Create a dictionary that maps section objects to sequential integers"""
#    def __init__(self, morph):
#        functor = lambda s: len(self.dict) + offset
#        super(SectionIndexerWithOffsetDF, self).__init__(morph=morph, functor=functor)


class SectionListerDF(ListBuilderSectionVisitor):
    def __init__(self, morph):
        functor = lambda s: s
        super(SectionListerDF, self).__init__(morph=morph, functor=functor)



















