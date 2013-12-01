





from morphforge.core import LocMgr, Join
from morphforge.morphology.ui import MatPlotLibViewer
from morphforge.morphology.core import MorphologyTree

testSrcsPath = LocMgr().get_test_srcs_path()
srcSWCFile = Join(testSrcsPath, "swc_files/28o_spindle20aFI.CNG.swc")

m = MorphologyTree.fromSWC(src=open(srcSWCFile))
MatPlotLibViewer(m, use_pca=False)
MatPlotLibViewer(m, use_pca=True)

