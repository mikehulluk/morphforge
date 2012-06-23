#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
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
#import quantities as pq

import operator
#from tracetypes import Trace_FixedDT
#from traceGenerator import NpPqWrappers


class TraceOperatorCtrl(object):
    trace_operators_all = {}
    trace_operators_active = {}
    trace_operators = [ operator.__add__,
                        operator.__sub__,
                        operator.__div__,
                        operator.__mul__ ]

    @classmethod
    def add_trace_operator( cls, operator_type, lhs_type, rhs_type, operator_func, flag='default', set_as_default=False):
        #toc = TraceOperatorCtrl
        assert operator_type in cls.trace_operators

        key = ( operator_type, lhs_type, rhs_type)

        # Add to the list of all:
        if not key in cls.trace_operators_all:
            cls.trace_operators_all[key] = {}

        # Check the flag is not already active:
        assert not flag in cls.trace_operators_all[key]
        cls.trace_operators_all[key][flag] = operator_func

        # Set as default if there is no current default, or flag is default:
        if not key in cls.trace_operators_active or flag=='default' or set_as_default:
            cls.trace_operators_active[key] = operator_func, flag

    @classmethod
    def add_trace_operator_symmetrical( cls, operator_type, lrhs_type, operator_func, flag='default', set_as_default=False):
        cls.add_trace_operator( operator_type=operator_type,
                              lhs_type=lrhs_type,
                              rhs_type=lrhs_type,
                              operator_func=operator_func,
                              flag=flag,
                              set_as_default=set_as_default)


    #@classmethod
    #def set_active_trace_operator( cls, operator_type, lhs_type, rhs_type, flag ):
    #    assert False, 'Deprecated'
    #    key = ( operator_type, lhs_type, rhs_type)
    #    assert flag in TOC.trace_operators_all[key]
    #    TOC.trace_operators_active = TOC.trace_operators_all[key][flag], flag




    @classmethod
    def operate( cls, operator_type, lhs, rhs, use_flag=None, **kwargs ):
        #toc = TraceOperatorCtrl
        key = operator_type, type(lhs), type(rhs)

        # Use the active operation:
        if not use_flag:
            assert key in cls.trace_operators_active, 'Trace Operation not defined for: %s' % str(key)
            opfunctor = cls.trace_operators_active[key][0]

        # Use a custom operation:
        else:
            assert key in cls.trace_operators_all
            assert use_flag in cls.trace_operators_all[key]
            opfunctor = cls.trace_operators_all[key][use_flag]


        return opfunctor(lhs=lhs, rhs=rhs, **kwargs)
