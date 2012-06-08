#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.  - Redistributions in
#  binary form must reproduce the above copyright notice, this list of
#  conditions and the following disclaimer in the documentation and/or other
#  materials provided with the distribution.
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
from utils import CleanFilename, EnsureDirectoryExists, ScriptUtils
import os

class FigTypes:
    EPS = "eps"
    SVG = "svg"
    PDF = "pdf"
    PNG = "png"


class PlotManager():
    figNum=0
    figures_saved = []
    figures_saved_filenames = []
    #def __init__(self):
    #    pass


    #defaultFilenameTmpl = """figures/${modulename}/fig${fignum:02d}_${figname}.${figtype}"""
    defaultFilenameTmpl = """_output/figures/{modulename}/{figtype}/fig{fignum:03d}_{figname}.{figtype}"""
    #defaultDirTmpl = """figures/{modulename}/"""
    defaultFigTypes = [FigTypes.EPS, FigTypes.PDF, FigTypes.PNG, FigTypes.SVG]



    @classmethod
    def SaveFigure(cls, figname="", figure=None, filenameTmpl=None, figtypes=None  ):

        import sys
        #print sys.modules.keys()
        if 'mplpaperconfig' in sys.modules.keys():
            PlotManager.defaultFigTypes = [FigTypes.SVG]

        #assert False

        import pylab
#        assert False
        if not filenameTmpl:
            filenameTmpl = cls.defaultFilenameTmpl
        if not figtypes:
            figtypes = cls.defaultFigTypes


        assert isinstance( figtypes, list )

        # Get the figure:
        f = figure if figure else pylab.gcf()

        f.subplots_adjust(bottom=0.15)

        # Find the module this function was called from:
        modulename = ScriptUtils.getCallingScriptFile(includeExt=False)


        #For each filetype:
        for figtype in figtypes:

            # Create the filename:
            substDict = {"modulename":modulename, "fignum":PlotManager.figNum, "figname":figname,"figtype":figtype}
            fName = filenameTmpl.format(**substDict)

            fName=fName.replace(":","=")
            assert not ":" in fName, 'For windows compatibility'

            fName = CleanFilename(fName)
            EnsureDirectoryExists(fName)


            # Save the figure:
            f.savefig(fName)
            PlotManager.figures_saved.append( f.number )
            pwd = os.getcwd()
            PlotManager.figures_saved_filenames.append( os.path.join(pwd, fName ) )
            print 'Saving File', fName
            #print 'Figs Saved', len( cls.figures_saved )

        #Increment the fignum:
        PlotManager.figNum = PlotManager.figNum + 1

    #@classmethod
    #def save_active_figures(cls):
    #    import matplotlib._pylab_helpers
    #    figures=[manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
    #    for f in figures:
    #        cls.SaveFigure(figure=f)

