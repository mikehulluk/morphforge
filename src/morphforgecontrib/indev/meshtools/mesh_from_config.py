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


xTest = """


COLOR_ALIASES {

    RB: (255,210,50);
    dlc: (255,0,0);
    dla: (255,170,140);
    tIN: (230,50,120);
    cIN: (0,170,220);
    aIN: (70,70,180);
    dIN: (150,80,30) ;
    MN: (0,150,60);

    UnknownRgn: (30,250,250);
}


COLOR_DEFAULTS {
    RegionColor 1 : (128,0,0);
    RegionColor 2,3,4 : (0,128,0);
}

COLOR_DEFAULTS {
    RegionColor 1 : (128,128,0);
    RegionColor 6,7: RB;
}

MAKEPLY "aIN 471.ply" {
    RegionColor 1 : aIN;
    RegionColor 9,10,13,14: IGNORE;
    }


MAKEPLY "aIN 471.ply" {
    RegionColor 5,15,16 : UnknownRgn;
    RegionColor 2 : aIN;
    RegionColor 1 : aIN;
    RegionColor 9,10,13,14: IGNORE;
    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:100} ;

    }

#MAKEPLY "aIN 471.ply" {
#    RegionColor * : aIN;
#    RegionColor 9,10,13,14: IGNORE;
#    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:50, OFFSET:(0,0,0) };
#    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:50, OFFSET:(0,0,20) };
#    Include "aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc" {TRIM:50, OFFSET:(0,0,40) };
#
#    }
#



"""

from mesh_config_parser import parse_zip_file
# parse_zip_file(zip_in ="/home/michael/Desktop/ply/src.zip",
#                zip_out = "/home/michael/Desktop/ply/fromPly.zip")

print 'A'
parse_zip_file(zip_in='/home/michael/Desktop/circuit2/src.zip',
               zip_out='/home/michael/Desktop/circuit2/src_out.zip')

