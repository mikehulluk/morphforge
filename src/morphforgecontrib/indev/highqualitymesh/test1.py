



from morphforge.core import LocMgr, Join
from morphforge.morphology.ui import MatPlotLibViewer
from morphforge.morphology.core import MorphologyTree
from morphforgecontrib.indev.highqualitymesh.create_mesh import MeshFromGTS
from morphforge.morphology.importer.import_array_swc import NewSWCLoader

testSrcsPath = LocMgr().get_test_srcs_path()
srcSWCFile = Join(testSrcsPath, "swc_srcs/28o_spindle20aFI.CNG.swc")



srcSWCFile = "/home/michael/Desktop/ply/forPly/aIN 471 nrn + ns 100325.transl.invX.scaled.straightened.swc"

#m = MorphologyTree.fromSWC(src=open(srcSWCFile))

morphs = NewSWCLoader.load_swc_set(src=open(srcSWCFile))

m = morphs[0]
m = m.to_tree()

mesh = MeshFromGTS.build(m)

#MatPlotLibViewer(m, use_pca=False)