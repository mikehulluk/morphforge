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


from enthought.traits.api import *
import wx









from enthought.traits.ui.api import View,Item,Group
from enthought.traits import *


import random

class MusicPlayer(HasStrictTraits):

# Music tracks.
    track = TraitPrefixList

    # Current time of the song in seconds.
    current_time = Range(0.0, 100.0)

    view = View('track', 'current_time')

    def set_songs(self, songs):
        trait = Trait(songs[0], TraitPrefixList(songs))
        self.add_trait('track', trait)

    def _track_changed(self, val):
    # Just set the current song's length to something random.
        rand_track_time = float(random.randrange(10, 1200))
        trait = Range(0.0, rand_track_time, 0)
        self.add_trait('current_time', trait)
        # Rebuild UI if needed.
        v = self.trait_view()
        v.updated = True
        print "Range should update to", 0, rand_track_time


player = MusicPlayer()
songs = ['wish you were here', 'time','smoke on the water', 'acknowledgement']
player.set_songs(songs)

player.track = 'time'
player.configure_traits()



class Counter(HasTraits):
    value =  Int()

    def __init__(self):

        self.add_trait('R', Range(0,10,1))

        v = self.trait_view()
        v.updated = True
        HasTraits.__init__(self)

#Counter().edit_traits()
Counter().configure_traits()

#wx.PySimpleApp().MainLoop()
