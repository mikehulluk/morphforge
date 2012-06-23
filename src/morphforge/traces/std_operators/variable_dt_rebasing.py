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
class VariableDTRebaseTimeValues(object):

    # Merge all the time indices, so twice the number of
    # times. this will we bad for things like: A+B+C+D+E+...
    @classmethod
    def All(cls, tr1, tr2):
        t1 = tr1._time.rescale("ms").magnitude
        t2 = tr2._time.rescale("ms").magnitude
        t = np.hstack( (t1,t2) )
        t = np.sort(t)
        return t * pq.ms

    @classmethod
    def MaintainMaximumDY(cls, tr1, tr2):
        assert False

    @classmethod
    def MaintainMinimumFrequency(cls, tr1,tr2):
        assert False

        # 1. Create a high density time grid,
        # all zeros except 1's at the time points of
        # tr1


        # 2. Convolve this grid with a longer 'envelop'
        # function. (Gaussian 3 times the length of the
        # longest dt step?
        # This gives a indication of instanteous frequency.

        # 3. Repeat for tr2

        # 4. Take the min on these two

        # 5. Recreate the times

