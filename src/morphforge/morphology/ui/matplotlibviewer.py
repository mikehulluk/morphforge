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
from morphmaths import MorphologyForRenderingOperator

from morphforge.morphology.visitor import DictBuilderSectionVisitorHomo

import numpy
import numpy as np

import pylab
from matplotlib.path import Path
from matplotlib import patches



class MatPlotLibViewer(object):
    """
    Plot Projections of a morphology onto XY, XZ, and YZ axes.
    """
    
    plotViews = [0,1,2]
    
    
    projMatXY = numpy.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0 ], [0.0, 0.0, 1.0 ]])
    projMatXZ = numpy.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0 ], [1.0, 0.0, 0.0 ]])
    projMatYZ = numpy.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0 ], [0.0, 1.0, 0.0 ]])
    
    figureProjections = {0:projMatXY, 1:projMatXZ, 2:projMatYZ}
    figureLabels = {0:("X", "Y"), 1:("Z", "Y"), 2:("X", "Z")}
    figurePositions = {0:221, 1:222, 2:223}
    figureTitles = { 0:"View From Above", 1:"View From Side", 2:"View From Front"}
    
    
    #plotViews = [0,]
    #figurePositions = {0:111, 1:111, 2:111}
    
    def __init__(self, morph, use_pca=True):
        
        if morph == None: raise ValueError("No Cell")
        
        self.morph = morph
        
        self.fig = None
        self.subplots = {}
        
        self.buildPlot(use_pca)
    
        
        
    
    
    def buildDrawSubPlot(self, rotatedSectionDict, fig, i, plotLims):
        
        
        subplotnum = self.figurePositions[i]
        title = self.figureTitles[i]
        projMatrix = self.figureProjections[i]
        labels = self.figureLabels[i]
        
        
        ax = fig.add_subplot(subplotnum, aspect='equal')
        
        
        #Find the depth extremes for coloring:
        zMin, zMax = None, None
        for seg in self.morph:
            xyzProj = numpy.dot(projMatrix, rotatedSectionDict[seg])
            zMin = xyzProj[2] if not zMin else min(zMin, xyzProj[2])
            zMax = xyzProj[2] if not zMax else max(zMax, xyzProj[2])
        zRange = zMax - zMin
        
        
        for seg in self.morph:   
            xyzProj = numpy.dot(projMatrix, rotatedSectionDict[seg])
            xyProj = numpy.array([xyzProj[0], xyzProj[1]])
            
            xyzProjParent = numpy.dot(projMatrix, rotatedSectionDict[seg.parent])
            xyProjParent = numpy.array([xyzProjParent[0], xyzProjParent[1]])
            
            color = str((xyzProj[2] - zMin) / zRange) if zRange > 0.001 else 'grey' 
            
            linewidth = ( ( seg.d_r+seg.p_r)/2.0) *2.0
            
            #Test if we have just tried to draw a point, if so then draw a circle:
            if numpy.linalg.norm(xyProj - xyProjParent) < 0.0001:
                try: 
                    ax.add_patch(pylab.Circle(xyProj, radius=linewidth, color=color))
                    ax.plot(xyProj[0], xyProj[1], '+', markersize=linewidth, color='red')
                except:
                    pass
            else:
                
                # Simple version, which doesn't work so well:
                #ax.plot([xyProj[0], xyProjParent[0]], [xyProj[1], xyProjParent[1]], linewidth=linewidth, color=color)
                
                # More complex patch version:
                joiningVec = xyProj - xyProjParent
                joiningVecNorm = joiningVec / numpy.linalg.norm(joiningVec)

                perpVec = np.array( (joiningVecNorm[1],joiningVecNorm[0] * -1) )
                
                assert( np.fabs(np.dot(joiningVecNorm, perpVec ) ) < 0.01)
                
                # The points:
                p1 = xyProj + ( perpVec * seg.d_r)
                p2 = xyProj - ( perpVec * seg.d_r) 
                
                p3 = xyProjParent - ( perpVec * seg.p_r)
                p4 = xyProjParent + ( perpVec * seg.p_r)
                
                verts = [p1,p2,p3,p4,(0,0)]
                codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY, ]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor=color, lw=1)
                ax.add_patch(patch)
                
            
        
        
        ax.set_title(title)
        ax.set_xlim(plotLims)
        ax.set_ylim(plotLims)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.grid(True)
        return ax  
        
        
    def buildPlot(self, usePCA):
        
        
        self.normaliser = MorphologyForRenderingOperator(self.morph, usePCA=usePCA)
        
        # Find the Point that is the furthest distance way from 
        # the centre when the cell is centred and rotated:
        rotator = lambda s: self.normaliser(s.getDistalNPA3())
        
        rotatedSectionDict = DictBuilderSectionVisitorHomo(morph=self.morph, functor=rotator ) ()
        
        # Add in the parents manually:
        p = self.morph._dummysection 
        rotatedSectionDict[ p ] = self.normaliser( p.getDistalNPA3() )
 
        
        
        maxAxis = max([ numpy.linalg.norm(rs) for rs in rotatedSectionDict.values() ])
        plotLims = (maxAxis * -1.1, maxAxis * 1.1)
        
        maxX = max([ numpy.fabs(rs[0]) for rs in rotatedSectionDict.values() ])
        maxY = max([ numpy.fabs(rs[1]) for rs in rotatedSectionDict.values() ])
        maxZ = max([ numpy.fabs(rs[2]) for rs in rotatedSectionDict.values() ]) 
        
        maxes = [maxX, maxY, maxZ]
        
        #allMax = max(maxes)
        for i in self.plotViews: 
            maxes[i] = maxes[i] + 0.2 * max([maxX, maxY, maxZ]) 
        
        
               
        
        
        
        
        
        
        self.fig = pylab.figure(figsize=(7, 7))
        self.fig.subplots_adjust(left=0.05, top=0.95, right=0.95, bottom=0.05, wspace=0.1, hspace=0.1)



        
        self.subplots = {}
        for i in self.plotViews:
            self.subplots[i] = self.buildDrawSubPlot(rotatedSectionDict, self.fig, i, plotLims)
        
        
        
        
