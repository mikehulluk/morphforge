








from morphforge.morphology.core import MorphologyArray
from StringIO import StringIO

swcSrc = """
1 0 1.0 2.0 3.0 4.0 -1
2 0 5.0 6.0 7.0 8.0 1
"""

m = MorphologyArray.fromSWC(StringIO(swcSrc))

print 'Morphology Vertices:'
print m._vertices

print 'Morphology Connectivity:'
print m._connectivity


