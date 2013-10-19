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

import numpy
import random


class MFRandom(object):

    """ A class to centralise random numbers.

    This is centralised so that a seed can be set in a single place in order
    to make simulations repeatable. This is particularly relevant in the case
    of NEURON simulations, which are saved and spawned in another process.
    """

    _seed = None

    @classmethod
    def seed(cls, seed):
        """ Seed the random number generator

        This method simply calls 'random.seed()' and 'numpy.random.seed()'
        """

        MFRandom._seed = seed
        cls._reseed()

    @classmethod
    def get_seed(cls):
        """ Returns the current seed used"""

        return cls._seed

    @classmethod
    def _reseed(cls):
        random.seed(cls._seed)
        numpy.random.seed(cls._seed)


import os
if not os.environ.get('READTHEDOCS', None) == 'True':
    # Randomly initialise the seed:
    MFRandom.seed(random.randint(0, 100000))
