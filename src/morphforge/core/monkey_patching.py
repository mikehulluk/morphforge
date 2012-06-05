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

import os

from morphforge.core.mgrs import SettingsMgr, LogMgr
from mhlibs.scripttools.plotmanager import PlotManager


# Used to supress pyflakes errors:
def my_pass(*args,**kwargs):
    pass




class SavedFigures(object):
    nums = set()


def saveAllNewActiveFigures():
    import matplotlib

    active_figures=[manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
    active_new_figures = [ a for a in active_figures if not a.number in SavedFigures.nums]

    # Add to the list of saved figures
    [SavedFigures.nums.add(a.number) for a in active_figures ]

    # Save the new figures:
    for a in active_new_figures:
        if a.number in PlotManager.figures_saved:
            continue

        PlotManager.SaveFigure(figname='AutoSaveFigure_%d'%a.number, figure=a)




# Monkey-Patch pylab, unless we are on read-the-docs
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:

    # Matplotlib:
    import matplotlib
    if not os.environ.get('DISPLAY',None):
        matplotlib.use('Agg')


    # patch mpl.show()
    import pylab
    mplShow = matplotlib.pylab.show
    def show(*args, **kwargs):
        saveAllNewActiveFigures()
        if SettingsMgr.showGUI():
            LogMgr.info("mpl.show() call made")
            mplShow(*args, **kwargs)

        else:
            LogMgr.info("mpl.show() call not made")
    matplotlib.pylab.show = show
    pylab.show = show


    # patch mpl.savefig
    #  - Make sure that the directory actually exists:
    mplsavefig = matplotlib.pylab.show
    def savefig(filename, *args, **kwargs):
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        return mplsavefig(filename, *args, **kwargs)
    matplotlib.pylab.savefig = savefig
    pylab.savefig = savefig




# Shall we automatically start coverage testing:
if "MF_TEST_COVERAGE" in os.environ:
    #assert False
    coverage_opdir = '/tmp/morphforge_coverage_output'
    if not os.path.exists(coverage_opdir):
        os.makedirs(coverage_opdir)
    os.environ['COVERAGE_PROCESS_START']="/home/michael/hw_to_come/morphforge/etc/.coveragerc"
    import coverage
    coverage.process_startup()







# Decorate simulations; to record running times and
# catch unhandled exceptioms:
if SettingsMgr.DecorateSimulations():
    print 'Decorating Simulation'
    from mhlibs.simulation_manager.simulation_hooks import db_writer_hook
    db_writer_hook.SimulationDecorator.Init()







# MayaVI
def MonkeyPatchMayaVi():
    print 'Monkey Patching Mayavi'

    #import enthought.mayavi.mlab as mlab
    import mayavi
    from mayavi import mlab
    my_pass(mlab)




# Set-up the defaul priting:
import numpy as np
np.set_printoptions(precision=2)



