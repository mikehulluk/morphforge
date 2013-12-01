





from morphforge.core import LocMgr, Join
from morphforge.morphology.core import MorphologyTree


testSrcsPath = LocMgr().get_test_srcs_path()
srcSWCFile = Join(testSrcsPath, "swc_files/28o_spindle20aFI.CNG.swc")

mTree = MorphologyTree.fromSWC(src=open(srcSWCFile))
mArray = mTree.to_array()

print 'Vertex Data'
print mArray._vertices


# Convert back
mTree2 = mArray.to_tree()

# Round-trip: check that the SWC outputs are the same:
assert mTree.toSWCStr() == mTree2.toSWCStr()
print 'Finished OK'




