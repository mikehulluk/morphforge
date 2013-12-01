




from morphforge.morphology import MorphologyTree


# Build a morphology consisting of a single-section:
morphDict1 = {'root': {'length': 20, 'diam': 20} }
m1 = MorphologyTree.fromDictionary(morphDict1, name="SimpleMorphology1")
print "M1:"
for section in m1:
    print section


# Build a morphology consisting of a 2 compartments:
morphDict2 = {'root': {'length': 20, 'diam': 20, 'sections': [{'length': 300, 'diam': 2}]  } }
m2 = MorphologyTree.fromDictionary(morphDict2, name="SimpleMorphology2")
print "M2:"
for section in m2:
    print "Section:"
    print " - Proximal:", section.p_x, section.p_y, section.p_z, section.p_r
    print " - Distal:  ", section.d_x, section.d_y, section.d_z, section.d_r

