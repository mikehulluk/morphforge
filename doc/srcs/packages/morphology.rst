

morphforge.morphology
---------------------

.. automodule:: morphforge.morphology





morphforge.morphology.core
===========================

.. automodule:: morphforge.morphology.core
    :no-members:
    
.. toctree::
 
    /srcs/details/morphology_details


.. autosummary::
   :toctree: DIRNAME
   
    morphforge.morphology.core.MorphologyTree
    morphforge.morphology.core.Section
    morphforge.morphology.core.Region
    morphforge.morphology.core.MorphLocation 
    morphforge.morphology.core.MorphPath

   
     
morphforge.morphology.builders
===================================

.. automodule:: morphforge.morphology.builders
    :no-members:

.. autosummary::
   :toctree: DIRNAME
   
    morphforge.morphology.builders.MorphologyBuilder
    
    


morphforge.morphology.comparison
=====================================

.. automodule:: morphforge.morphology.comparison
    :no-members:


.. autosummary::
   :toctree: DIRNAME
   
    morphforge.morphology.comparison.MorphologyConverter


morphforge.morphology.conventions
=====================================

.. automodule:: morphforge.morphology.conventions
    :no-members:


.. autosummary::
   :toctree: DIRNAME
   
    morphforge.morphology.conventions.StdRegions
    morphforge.morphology.conventions.SWCRegionCodes

   

morphforge.morphology.conversion
=====================================

.. automodule:: morphforge.morphology.conversion
    :no-members:


.. autosummary::
   :toctree: DIRNAME
   
    morphforge.morphology.conversion.RegionToIntMapBiMap
    morphforge.morphology.conversion.AutoRegionToIntMapTable



morphforge.morphology.errors
=====================================

.. automodule:: morphforge.morphology.errors
    :no-members:

.. autosummary::
   :toctree: DIRNAME
   
    morphforge.morphology.errors.MorphologyImportError
    morphforge.morphology.errors.MorphologyExportError
    morphforge.morphology.errors.MorphologyFrameworkRegistrationError


morphforge.morphology.exporter
==================================

.. automodule:: morphforge.morphology.exporter
    :no-members:

.. autosummary::
   :toctree: DIRNAME

   morphforge.morphology.exporter.MorphologyExporter(object):
   morphforge.morphology.exporter.ExportArray_SWC():
   morphforge.morphology.exporter.SWCTreeWriter(object):


morphforge.morphology.importer
==================================
  NewSWCLoader(object):

  DictionaryLoader(object):

   MorphologyImporter(object):

[*] morphforge.morphology.mesh
==============================
   69 : class MeshBuilderRings(object):
./mesh/mesh.py:
   36 : class TriangleMesh(object):
./mesh/writer_ply.py:
   37 : class MeshWriterPLY(object):


[*] morphforge.morphology.util
==================================
   31 : class MorphLocator(object):


[*] morphforge.morphology.ui
==================================
   43 : class MatPlotLibViewer(object):
./ui/mayavirenderer.py:
   48 : class MayaViRenderer(object):


[*] morphforge.morphology.visitor
==================================
   45 : class SectionVisitorDF(object):
  112 : class SectionVisitorDFOverrider(SectionVisitorDF):
  126 : class SectionVisitorHomogenousOverrider(SectionVisitorDFOverrider):
  146 : class DictBuilderSectionVisitorHomo(SectionVisitorHomogenousOverrider):
  157 : class ListBuilderSectionVisitor(SectionVisitorDF):
  175 : #class NumpyBuilderSectionVisitor(SectionVisitorDF):
  207 : class SectionIndexerDF(DictBuilderSectionVisitorHomo):
  216 : # I reckon this can probably be combined into the class above, but I have not tried it yet!
  217 : #class SectionIndexerWithOffsetDF(DictBuilderSectionVisitor):
  225 : class SectionListerDF(ListBuilderSectionVisitor):
./visitor/visitorfactory.py:
   40 : class SectionVistorFactory(object):



.. automodule:: morphforge.morphology
