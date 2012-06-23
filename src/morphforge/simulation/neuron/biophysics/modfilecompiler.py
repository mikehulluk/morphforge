#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
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

from morphforge.core import  FileIO, LocMgr, LogMgr
from morphforge.core import Join, Exists, Basename

from morphforge.core import RCMgr as RCReader

import os
import subprocess


import shutil
from morphforge.core.mgrs.settingsmgr import SettingsMgr





#TODO! NOTE THE LINKING LIBRARY ORDER HAS CHANGED!

class ModBuilderParams(object):
    nocmodlpath = RCReader.get("Neuron", "nocmodlpath")
    libtoolpath = RCReader.get("Neuron", "libtoolpath")

    compileIncludes = ['.', '..'] + RCReader.get("Neuron", "compileincludes").split(":")
    compileDefs = ["HAVE_CONFIG_H"]

    stdLinkLibs = ["nrnoc", "oc", "memacs", "nrnmpi", "scopmath", "sparse13", "readline", "ncurses", "ivoc", "neuron_gnu", "meschach", "sundials", "m", "dl", ]
    nrnLinkDirs = RCReader.get("Neuron", "nrnLinkDirs").split(":")

    #TODO: Find src of this:
    rpath = RCReader.get("Neuron", "rpath")
    rndAloneLinkStatement = RCReader.get("Neuron", "rndAloneLinkStatement")


    modlunitpath = RCReader.get("Neuron","modlunitpath")




    @classmethod
    def get_compile_str(cls, c_filename, lo_filename, additional_compile_flags=""):
        inclStr = " ".join(["""-I"%s" """ % s for s in cls.compileIncludes])
        defStr = " ".join(["""-D%s """ % d for d in cls.compileDefs])
        vars = {"lo":lo_filename, "c":c_filename, "incs":inclStr, "defs":defStr, 'additional_flags':additional_compile_flags}
        return """--mode=compile gcc %(defs)s  %(incs)s %(additional_flags)s  -g -O2 -c -o %(lo)s %(c)s  """ % vars


    @classmethod
    def get_link_str(cls, lo_filename, la_filename, additional_link_flags=""):
        stdLibStr = " ".join(["-l%s" % s for s in cls.stdLinkLibs])
        stdLibDirStr = " ".join(["-L%s" % s for s in cls.nrnLinkDirs])
        linkDict = {"la":la_filename,
                    "lo":lo_filename,
                    "stdLibStr":stdLibStr,
                    "stdLibDirStr":stdLibDirStr,
                    "rpath":cls.rpath,
                    "randSt": cls.rndAloneLinkStatement,
                    'additional_flags':additional_link_flags
                    }
        return """--mode=link gcc -module  -g -O2  -shared  -o %(la)s  -rpath %(rpath)s  %(lo)s  %(stdLibDirStr)s  %(randSt)s  %(stdLibStr)s  %(additional_flags)s """ % linkDict










def _simple_exec(cmd, remaining):
    print 'Executing: %s %s'%(cmd,remaining)
    output = subprocess.Popen([cmd + " " + remaining], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    if SettingsMgr.simulator_is_verbose():
        print output
    return output



def _build_modfile_local(mod_filename_short, modfile=None):
    print os.getcwd()
    modFileBasename = mod_filename_short.replace(".mod", "")
    c_filename = modFileBasename + ".c"
    la_filename = modFileBasename + ".la"
    lo_filename = modFileBasename + ".lo"
    soFilename = modFileBasename + ".so"

    libsDir = ".libs/"

    # Check for some existing files:
    gen_files = (libsDir, c_filename, la_filename, lo_filename, soFilename)
    for gen_file in gen_files:
        if Exists(gen_file):
            LocMgr.BackupDirectory(gen_file)


    #if Exists(libsDir): LocMgr.BackupDirectory(libsDir)
    #if Exists(c_filename): LocMgr.BackupDirectory(c_filename)
    #if Exists(la_filename): LocMgr.BackupDirectory(la_filename)
    #if Exists(lo_filename): LocMgr.BackupDirectory(lo_filename)
    #if Exists(soFilename): LocMgr.BackupDirectory(soFilename)



    #run nocmodl: .mod -> .c
    c_filename = modFileBasename + ".c"
    op  = _simple_exec(ModBuilderParams.nocmodlpath, mod_filename_short)

    if not Exists(c_filename):
        print "Failed to compile modfile. Error:"
        print op, "\n"
        assert False

    #Add the extra registration function into our mod file:
    newRegisterFunc = """\n modl_reg(){ _%s_reg(); }""" % (modFileBasename)
    FileIO.append_to_file(newRegisterFunc, c_filename)


    #Compile the .c file -> .so:
    compileStr = ModBuilderParams.get_compile_str(c_filename, lo_filename)
    linkStr = ModBuilderParams.get_link_str(lo_filename, la_filename)

    if SettingsMgr.simulator_is_verbose():
        print 'IN:',ModBuilderParams.libtoolpath,
        print compileStr
        print linkStr

    compile_flags = modfile.additional_compile_flags if modfile else ""
    link_flags = modfile.additional_link_flags if modfile else ""
    op1 = _simple_exec(ModBuilderParams.libtoolpath, ModBuilderParams.get_compile_str(c_filename, lo_filename,additional_compile_flags=compile_flags))
    op2 = _simple_exec(ModBuilderParams.libtoolpath, ModBuilderParams.get_link_str(lo_filename, la_filename, additional_link_flags=link_flags))

    if SettingsMgr.simulator_is_verbose() or True:
        print "OP1:", op1
        print "OP2:", op2

    # Copy the correct .so from the libDir to the build_dir:
    shutil.move(Join(libsDir, modFileBasename + ".so.0.0.0"), soFilename)


    #Clean up:
    if True:
        os.remove(c_filename)
        os.remove(mod_filename_short)
        for f in [".la", ".lo"]:
            os.remove(modFileBasename + f)
        for f in [".la", ".lai", ".o", ".so", ".so.0" ]:
            os.remove(Join(libsDir, modFileBasename + f))
        os.rmdir(libsDir)


    return soFilename




def _build_mod_file(modfilename, output_dir=None, build_dir=None, modfile=None):

    build_dir = LocMgr().get_default_mod_builddir() if not build_dir else build_dir
    output_dir = LocMgr().get_default_mod_outdir() if not output_dir else output_dir

    if SettingsMgr.simulator_is_verbose():
        print " - Building: ", modfilename

    modfilenamebase = Basename(modfilename)
    sofilenamebase = modfilenamebase.replace(".mod", ".so")

    shutil.copyfile(modfilename, Join(build_dir, modfilenamebase))
    soFilenameOutput = Join(output_dir, sofilenamebase)

    # Move to new directory to build:
    initialCWD = os.getcwd()
    os.chdir(build_dir)
    soFilenameBuildShort = _build_modfile_local(mod_filename_short=modfilenamebase,modfile=modfile)
    os.chdir(initialCWD)

    # CopyFile to output location:
    soFilenameBuild = Join(build_dir, soFilenameBuildShort)
    if soFilenameBuild != soFilenameOutput:
        shutil.move(soFilenameBuild, soFilenameOutput)
    return soFilenameOutput












class ModFileCompiler(object):

    @classmethod
    def check_modfile_units(cls, modfilename):
        op = _simple_exec( ModBuilderParams.modlunitpath, modfilename )

        opExpected = """
        model   1.1.1.1   1994/10/12 17:22:51
        Checking units of %s""" % modfilename

        if SettingsMgr.simulator_is_verbose():
            print 'OP',op

        # Check line by line:
        for l, le in zip( op.split("\n"), opExpected.split("\n")  ):
            if not le.strip() == l.strip():
                print "ERROR ERROR ERROR WITH UNITS!!"
                print 'Seen', l
                print 'Expt', le
                #assert False


    @classmethod
    def _build_modfile(cls, modfile):
        outputFilename = modfile.get_built_filename_full(ensure_built=False)

        if not Exists(outputFilename):
            LogMgr.info("Does not exist: building: %s" % outputFilename)

            modTxtFilename = FileIO.write_to_file(modfile.modtxt, suffix=".mod")
            ModFileCompiler.check_modfile_units(modTxtFilename)
            modDynFilename = _build_mod_file(modTxtFilename, modfile=modfile)
            shutil.move(modDynFilename, outputFilename)


        else:
            LogMgr.info("Already Built")
        return outputFilename

