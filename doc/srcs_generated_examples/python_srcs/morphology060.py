




import morphforge.stdimports as mf
import pylab

# Load a morphology from an SWC File, and look at the surface area and
# volume of the different section types
testSrcsPath = mf.LocMgr().get_test_srcs_path()
srcSWCFile = mf.Join(testSrcsPath, "swc_files/28o_spindle20aFI.CNG.swc")
morph = mf.MorphologyTree.fromSWC(src=open(srcSWCFile))


#Look at the regions that are used in this morphology:
for region in  morph.get_regions():
    #print region
    print "Region: %s (%d)"%(region.name, 0)# len(region))
    print " - Surface Area: ", sum([section.area for section in region]), "um2"
    print " - Volume: ", sum([section.volume for section in region]), "um3"




# (Simple, but not the most efficient way to
# to this. For illustration purposes:)

def section_dist_to_dummy(sect):
    if sect.is_dummy_section(): return 0.0
    return section_dist_to_dummy(sect.parent) + sect.get_length()

f = pylab.figure()

ax1 = f.add_subplot("111")
ax1.set_xlabel("Distance from soma")
ax1.set_ylabel("Radius")
ax1.set_color_cycle(['red','blue'])
for region in  morph.get_regions():
    sections = list(region.sections)

    dists = [section_dist_to_dummy(s) for s in sections]
    radii = [s.d_r for s in sections]

    ax1.plot(dists, radii, 'o', label="Region: %s" % region.name)

ax1.legend()
pylab.show()

