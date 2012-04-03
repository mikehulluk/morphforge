
2. Loading from SWC and rendering with Matplotlib
=================================================



Loading from SWC and rendering with Matplotlib.
This example shows loading in a morphology from an SWC file and then viewing it in matplotlib, 
using Principle Component Analysis (PCA) to align the features of the morphology to the plot 
window.  



Code
~~~~

.. code-block:: python

	
	
	
	"""Loading from SWC and rendering with Matplotlib.
	This example shows loading in a morphology from an SWC file and then viewing it in matplotlib, 
	using Principle Component Analysis (PCA) to align the features of the morphology to the plot 
	window.  
	"""
	
	from morphforge.core import LocMgr, Join 
	from morphforge.morphology.ui import MatPlotLibViewer
	from morphforge.morphology.core import MorphologyTree
	
	
	testSrcsPath = LocMgr().getTestSrcsPath()
	srcSWCFile = Join(testSrcsPath, "swc_srcs/28o_spindle20aFI.CNG.swc")
	
	m = MorphologyTree.fromSWC(src=open(srcSWCFile))
	MatPlotLibViewer(m, use_pca=False)
	MatPlotLibViewer(m, use_pca=True)
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 83717
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/morphology020_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/morphology020_out1.png>`


.. figure:: /srcs_generated_examples/images/morphology020_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/morphology020_out2.png>`



