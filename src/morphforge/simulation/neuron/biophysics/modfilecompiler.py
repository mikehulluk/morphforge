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

import os
import subprocess
import shutil

from morphforge.core import FileIO, LocMgr, LogMgr
from morphforge.core import RCMgr as RCReader
from morphforge.core.mgrs.settingsmgr import SettingsMgr



class ModBuilderParams(object):

    nocmodlpath = RCReader.get('Neuron', 'nocmodlpath')
    libtoolpath = RCReader.get('Neuron', 'libtoolpath')

    compile_includes = ['.', '..'] + \
                      RCReader.get('Neuron', 'compileincludes').split(':')

    compile_defs = ['HAVE_CONFIG_H']

    std_link_libs = [
        'nrnoc',
        'oc',
        'memacs',
        'nrnmpi',
        'scopmath',
        'sparse13',
        'readline',
        'ncurses',
        'ivoc',
        'neuron_gnu',
        'meschach',
        'sundials',
        'm',
        'dl',
        ]
    nrn_link_dirs = RCReader.get('Neuron', 'nrnlinkdirs').split(':')

    rpath = RCReader.get('Neuron', 'rpath')
    rnd_alone_link_statement = RCReader.get('Neuron', 'rndalonelinkstatement')

    modlunitpath = RCReader.get('Neuron', 'modlunitpath')

    @classmethod
    def get_compile_str(cls, c_filename, lo_filename, additional_compile_flags=''):
        incl_str = ' '.join(["""-I"%s" """ % _incl for _incl in cls.compile_includes])
        def_str = ' '.join(["""-D%s """ % _def for _def in cls.compile_defs])
        variables = {'lo': lo_filename, 'c': c_filename, 'incs': incl_str, 'defs': def_str, 'additional_flags': additional_compile_flags}
        return """--mode=compile gcc %(defs)s  %(incs)s %(additional_flags)s  -g -O2 -c -o %(lo)s %(c)s  """ % variables


    @classmethod
    def get_link_str(cls, lo_filename, la_filename, additional_link_flags=''):
        std_lib_str = ' '.join(['-l%s' % lib for lib in cls.std_link_libs])
        std_lib_dir_str = ' '.join(['-L%s' % _dir for _dir in cls.nrn_link_dirs])
        link_dict = {'la': la_filename,
                    'lo': lo_filename,
                    'std_lib_str': std_lib_str,
                    'std_lib_dir_str': std_lib_dir_str,
                    'rpath': cls.rpath,
                    'randSt': cls.rnd_alone_link_statement,
                    'additional_flags': additional_link_flags
                    }
        return """--mode=link gcc -module  -g -O2  -shared  -o %(la)s  -rpath %(rpath)s  %(lo)s  %(std_lib_dir_str)s  %(randSt)s  %(std_lib_str)s  %(additional_flags)s """ % link_dict










def _simple_exec(cmd, remaining, err_ok=False):
    print 'Executing: %s %s' % (cmd, remaining)
    args = [cmd + ' ' + remaining]
    
    proc = subprocess.Popen(args,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    output = proc.communicate()[0]
    assert proc.returncode== 0 or err_ok==True, 'Problem Building Mod-file!' + '\n %s '% args

    if SettingsMgr.simulator_is_verbose():
        print output
    return output





def _build_modfile_local(mod_filename_short, modfile=None):
    print os.getcwd()
    mod_file_basename = mod_filename_short.replace('.mod', '')
    c_filename = mod_file_basename + '.c'
    la_filename = mod_file_basename + '.la'
    lo_filename = mod_file_basename + '.lo'
    so_filename = mod_file_basename + '.so'

    libs_dir = '.libs/'


    c_filename = mod_file_basename + '.c'
    output = _simple_exec(ModBuilderParams.nocmodlpath, mod_filename_short, err_ok=True)

    if not os.path.exists(c_filename):
        print 'Failed to compile modfile. Error:'
        print output, '\n'
        assert False

    # Add the extra registration function into our mod file:

    new_register_func = """\n modl_reg(){ _%s_reg(); }""" \
        % mod_file_basename
    FileIO.append_to_file(new_register_func, c_filename)

    # Compile the .c file -> .so:
    compile_str = ModBuilderParams.get_compile_str(c_filename, lo_filename)
    link_str = ModBuilderParams.get_link_str(lo_filename, la_filename)
    compile_flags = modfile.additional_compile_flags if modfile else ''
    link_flags = modfile.additional_link_flags if modfile else ''




    if SettingsMgr.simulator_is_verbose():
        print 'IN:', ModBuilderParams.libtoolpath,
        print compile_str
        print link_str

    op1 = _simple_exec(ModBuilderParams.libtoolpath, ModBuilderParams.get_compile_str(c_filename, lo_filename, additional_compile_flags=compile_flags))
    op2 = _simple_exec(ModBuilderParams.libtoolpath, ModBuilderParams.get_link_str(lo_filename, la_filename, additional_link_flags=link_flags))

    for filename in [c_filename, lo_filename, la_filename]:
        if not os.path.exists(filename):
            assert False, 'Error building mod-file!'


    if SettingsMgr.simulator_is_verbose() or True:
        print 'OP1:', op1
        print 'OP2:', op2

    # Copy the correct .so from the libDir to the build_dir:
    shutil.move(
        os.path.join(libs_dir, mod_file_basename + '.so.0.0.0'),
        so_filename)


    # Clean up:
    if True:
        os.remove(c_filename)
        os.remove(mod_filename_short)
        for ext in ['.la', '.lo']:
            os.remove(mod_file_basename + ext)
        for ext in ['.la', '.lai', '.o', '.so', '.so.0']:
            os.remove(os.path.join(libs_dir, mod_file_basename + ext))
        os.rmdir(libs_dir)

    return so_filename




def _build_mod_file(modfilename, output_dir=None, build_dir=None, modfile=None):

    build_dir = LocMgr().get_default_mod_builddir() if not build_dir else build_dir
    output_dir = LocMgr().get_default_mod_outdir() if not output_dir else output_dir

    if SettingsMgr.simulator_is_verbose():
        print ' - Building: ', modfilename

    modfilenamebase = os.path.basename(modfilename)
    sofilenamebase = modfilenamebase.replace('.mod', '.so')

    shutil.copyfile(
        modfilename, 
        os.path.join(build_dir, modfilenamebase))

    so_filename_output = os.path.join(output_dir, sofilenamebase)

    # Move to new directory to build:
    initial_cwd = os.getcwd()
    os.chdir(build_dir)
    so_filename_build_short = _build_modfile_local(mod_filename_short=modfilenamebase, modfile=modfile)
    os.chdir(initial_cwd)

    # CopyFile to output cell_location:
    so_filename_build = os.path.join(build_dir, so_filename_build_short)
    if so_filename_build != so_filename_output:
        shutil.move(so_filename_build, so_filename_output)
    return so_filename_output


class ModFileCompiler(object):

    @classmethod
    def check_modfile_units(cls, modfilename):
        output = _simple_exec(ModBuilderParams.modlunitpath, modfilename, err_ok=True)

        op_expected = """
        model   1.1.1.1   1994/10/12 17:22:51
        Checking units of %s""" % modfilename

        if SettingsMgr.simulator_is_verbose():
            print 'OP', output

        # Check line by line:
        for (line, line_expected) in zip(output.split('\n'), op_expected.split('\n')):
            if not line_expected.strip() == line.strip():
                print 'ERROR ERROR ERROR WITH UNITS!!'
                print 'Seen', line
                print 'Expt', line_expected
                # assert False


    @classmethod
    def build_modfile(cls, modfile):
        output_filename = modfile.get_built_filename_full(ensure_built=False)

        if not os.path.exists(output_filename):
            LogMgr.info('Does not exist: building: %s'
                        % output_filename)

            mod_txt_filename = FileIO.write_to_file(modfile.modtxt, suffix='.mod')
            ModFileCompiler.check_modfile_units(mod_txt_filename)
            mod_dyn_filename = _build_mod_file(mod_txt_filename, modfile=modfile)
            shutil.move(mod_dyn_filename, output_filename)
        else:

            LogMgr.info('Already Built')
        return output_filename


