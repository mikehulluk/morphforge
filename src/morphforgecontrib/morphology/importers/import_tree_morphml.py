#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------



assert False, "Do not use this module ~ currently in development"

from morphforge.core.misc import SeqUtils


def _clean_name(name):
    newName = ""
    for c in name:
        if c in string.ascii_letters + string.digits:
            newName += c
    return newName

from morphforge.morphology.core import MorphologyTree , Section, Region

import xml.dom.minidom as XML  
from morphforge.core.misc import SeqUtils

import collections
from morphforge.morphology.importer.morphologyimporter import MorphologyImporter
              
isElement = lambda s: s.nodeType == s.ELEMENT_NODE
    
def isElementWithTag(tag): 
    return lambda s: isElement(s) and s.tagName.split(':')[-1] == tag

def Filter(seq, functor): 
    return filter(functor, seq) 

def getText(node):
    return "".join([n.data for n in node.childNodes if n.nodeType == n.TEXT_NODE ])  



def FilterChildrenByTag(node, tag):
    return Filter( node.childNodes, isElementWithTag(tag) )

def FilterExpectSingleChildrenByTag(node, tag):
    return SeqUtils.filter_expect_single( node.childNodes, isElementWithTag(tag) )
    


class SearchableSet(object):
  def __init__(self,  data=None):
    self.data = set()

    if data:
      for d in data:
        self.add(d)

  def add(self, obj):
    self.data.add(obj)

  #def __getitem__(self, **kwargs):
  #  return self.data[k]

  def getitem(self, *args, **kwargs):

    assert len(kwargs) == 1
    k = kwargs.keys()[0]
    v = kwargs[k]
    
    assert len(args) ==0
    if isinstance(k, collections.Callable):
      return SeqUtils.expect_single( [ k(o) for o in self.data ] )
  
  
    elif isinstance(k, basestring):
      return SeqUtils.expect_single( [ o for o in self.data if getattr(o,k) == v ] )
    else:
      print 'Unexpected Type of %s - %s'%(k, type(k) )
      assert False

  def keys(self, k):
    if isinstance(k, collections.Callable):
      return [ k(o) for o in self.data ]
    elif isinstance(k, basestring):
      return [ getattr(o,k) for o in self.data ]
    else:
      assert False

  def __str__(self):
      return 'Searchable Set:< %s >'%self.data

  #def __delitem__(self, k):
  #  del self.data[key]





    
class Level1NeuroMLRepresentation(object):
    def __init__(self, cellNode):
                
        self.cables = SearchableSet()
        self.cablegroups = SearchableSet()
        self.segments = SearchableSet()
        

        # Read the XML:
        
        # Start with the declared Cables:
        cablesNode = FilterExpectSingleChildrenByTag( cellNode, 'cables') 
        
        # Load the individual cable objects
        for cableNode in FilterChildrenByTag(cablesNode, "cable"):
          if cableNode.getAttribute('id') in self.cables.keys('cable_id'):
            continue

          cable = NeuroMLCable(cable_id=cableNode.getAttribute('id'), name=cablesNode.getAttribute('name') ) 
          self.cables.add(cable)

          # Does the cable belong to any groups?
          for group_node in Filter(cableNode.childNodes, isElementWithTag("group")):
            cablegroupname = getText(group_node)
            if not cablegroupname in self.cablegroups.keys('name'):
              self.cablegroups.add( NeuroMLCableGroup(name = cablegroupname) )
            self.cablegroups.getitem(name=cablegroupname).add_cable(cable)


        # Load the CableGroup Objects:
        for cableGroupNode in Filter(cablesNode.childNodes, isElementWithTag("cablegroup")):
            
            # Get, or create, the cable node:
            cablegroupname = cableGroupNode.getAttribute('name')
            if not cablegroupname in self.cablegroups.keys('name'):
              self.cablegroups.add( NeuroMLCableGroup(name = cablegroupname) )
            grp = self.cablegroups.getitem(name=cablegroupname)
            
            # Add the cable segments:
            for cableNode in Filter(cableGroupNode.childNodes, isElementWithTag("cable")):
                cableNodeID = cableNode.getAttribute('id')
                if not cableNodeID in self.cables.keys('cable_id'):
                    assert False
                cable = self.cables.getitem(cable_id=cableNodeID)
                grp.add_cable(cable)
                
        
        # Load the Segments Objects:
        segmentsNode = SeqUtils.filter_expect_single(cellNode.childNodes, isElementWithTag("segments"))
        for segmentNode in Filter(segmentsNode.childNodes, isElementWithTag("segment")):
            
            #Attributes:
            segment_id = segmentNode.getAttribute('id')
            parent_id = segmentNode.getAttribute('parent')
            cable_id = segmentNode.getAttribute('cable')
            cable = self.cables.getitem(cable_id=cable_id) if cable_id else None
        
            
            
            
            # Distal Information:
            distalNode = FilterExpectSingleChildrenByTag(segmentNode, 'distal')
            d_X, d_Y, d_Z, d_d = float( distalNode.getAttribute('x') ), float( distalNode.getAttribute('y') ), float( distalNode.getAttribute('z') ), float(  distalNode.getAttribute('diameter') )
            dInfo = (d_X,d_Y,d_Z,d_d)
            
            
            proximalNode = FilterChildrenByTag(segmentNode, 'proximal')
            
            
            # Root node:
            if not parent_id:
                assert proximalNode
                proximalNode = SeqUtils.expect_single(proximalNode)
                p_X, p_Y, p_Z, p_d = float(proximalNode.getAttribute('x') ), float( proximalNode.getAttribute('y') ), float( proximalNode.getAttribute('z') ), float( proximalNode.getAttribute('diameter') ) 
                pInfo = (p_X,p_Y,p_Z,p_d)
                segment = NeuroMLSegment(segment_id=segment_id, 
                                             distInfo=dInfo,
                                             proxInfo=pInfo, 
                                             parent=None,
                                             cable=cable )
            
            #Child Node:
            else:
                
                # Not the root node, but a proximal node is provided:
                if proximalNode:
                    
                    pInfo = (p_X,p_Y,p_Z,p_d)
                    
                    # Proximal node and NOT the root: 
                    if parent_id:
                        parentNode = self.segments.getitem(segment_id=parent_id)
                        parentDistalInfo =  parentNode.distInfo
                        eps = 0.01 
                        #assert fabs( parentDistalInfo[0] - pInfo[0] ) < eps
                        #assert fabs( parentDistalInfo[1] - pInfo[1] ) < eps
                        #assert fabs( parentDistalInfo[2] - pInfo[2] ) < eps
                        #assert fabs( parentDistalInfo[3] - pInfo[3] ) < eps
                    
                
                # Add the child node:
                segment = NeuroMLSegment(segment_id=segment_id, 
                                             distInfo=dInfo,
                                             proxInfo=pInfo, 
                                             parent=None,
                                             cable=cable )
                
            # Add the segment to groups?
            self.segments.add(segment)
                    
                    
                        
        





class NeuroMLCable(object):
  def __init__(self, cable_id, name,group=None):
    self.cable_id = cable_id
    self.name =name
    self.internal_divisions = None
    self.groups = set()

    if group:
      self.add_to_group(group)

  def add_to_group(self,group):
      self.groups.add(group)
      group.cables.add(self)

  def __repr__(self):
      return 'NeuroML Cable <id: %s, name: %s, Groups:[%s]> '%(self.cable_id,self.name, ','.join( str(g) for g in self.groups) )   
      


class NeuroMLCableGroup(object):
  def __init__(self, name):
    self.name = name 
    self.cables = set()

  def add_cable(self, cable):
    self.cables.add(cable)
    cable.groups.add(self)



class NeuroMLSegment(object):
  def __init__(self, segment_id, distInfo, proxInfo=None, parent=None, cable=None, ):
      
      assert not (proxInfo and parent)
      
      self.segment_id = segment_id
      self.distInfo =distInfo
      self.proxInfo = proxInfo
      
      self.parent=parent 
      self.cable=cable



class MorphMLLoader(object):
    
    @classmethod
    def Load(cls, neuroMLFileObj, regions = None):    
        
        """regions is a dictionary, which maps cable-groups to a Region name; this handles the
        case when there are multiple group tags in a MorphML document, since morphforge does not allow multiple regions'
        """
            
        
        doc = XML.parse(neuroMLFileObj).documentElement
        assert doc.tagName in ( "morphml", 'neuroml' ) 

           
        # Do the action:
        cellsNode = SeqUtils.filter_expect_single(doc.childNodes, filter_func=isElementWithTag("cells"))

        
        morphs = []
        for cellNode in Filter(cellsNode.childNodes, isElementWithTag("cell")):
            morph = cls.LoadCell(cellNode, regions=regions)
            morphs.append(morph)
        assert len(morphs) == 1
        return morphs[0]
        
        
    @classmethod
    def LoadCell(cls, cellNode, regions=None):
        cableIDToRegionName, segmentListInfo = cls.LoadCellDictionaries(cellNode, regions=regions)
        
        # Make all the regions:
        regionNames = list(set( Filter(cableIDToRegionName.values(), lambda e:e is not None )) )
        print 'RegionNames:', regionNames
        regionNamesClean = [ _clean_name(str(rgnName)) for rgnName in regionNames]
        
        rgns = [ Region(name=rgnName) for rgnName in regionNamesClean]
        rgnNameToRegionDict = dict([ (rgn.name, rgn) for rgn in rgns])
        cableIDToRegionDict = dict([ (cableId, rgnNameToRegionDict[_clean_name(rgnName)]) if rgnName is not None else (cableId,None) for cableId, rgnName in cableIDToRegionName.iteritems()  ])
        
        
        # Find the node without a parent:
        rN = SeqUtils.filter_expect_single(segmentListInfo.values(), lambda s: not s[3])
        
        
        #Recursively Construct by finding what should be attached to current structure:
        #(id, name, cable,parent,(px,py,pz,pDiam),(dx,dy,dz,dDiam) )
        #rDummy = Section(region=cableIDToRegionDict[rN[2]], x=rN[4][0], y=rN[4][1], z=rN[4][2], r=rN[4][3] / 2.0)
        rDummy = Section(region=None, x=rN[4][0], y=rN[4][1], z=rN[4][2], r=rN[4][3] / 2.0)
        rActual = rDummy.create_distal_section(region=cableIDToRegionDict[rN[2]], x=rN[5][0], y=rN[5][1], z=rN[5][2], r=rN[5][3] / 2.0, idTag=rN[1]) 
        
        idToSectionMap = {rN[0]:rActual}
        recentlyAdded = [rN[0]]
        while recentlyAdded != []:
            curNode = recentlyAdded[0][0]
            curSect = idToSectionMap[curNode]
            recentlyAdded = recentlyAdded[1:]
            
            childNodes = Filter(segmentListInfo.values(), lambda s: s[3] == curNode)
            for c in childNodes:
                #print c
                newSect = curSect.create_distal_section(region=cableIDToRegionDict[c[2]], x=c[5][0], y=c[5][1], z=c[5][2], r=c[5][3] / 2.0, idTag=c[1]) 
                idToSectionMap[ c[0] ] = newSect
                recentlyAdded.append(c)
        
        return MorphologyTree(name="FromNeuroML", dummysection=rDummy, metadata={})
        
        
        
    @classmethod        
    def LoadCellDictionaries(self, cellNode, regions=None):


        l1 = Level1NeuroMLRepresentation(cellNode)
        
        




        print 'CellName:', cellNode.getAttribute('name')
        
        # We are not too worried about cables, but we do need the region name out of them:
        cableIDToRegionName = {}
        cablesNode = SeqUtils.filter_expect_single(cellNode.childNodes, isElementWithTag("cables"))
        for cableNode in Filter(cablesNode.childNodes, isElementWithTag("cable")):
            id = cableNode.getAttribute("id")
            name = cableNode.getAttribute("name")
            
            group_nodes = Filter(cableNode.childNodes, isElementWithTag("group"))
            
            if group_nodes:
                if regions:
                    metaGroupNode = SeqUtils.filter_expect_single(group_nodes, lambda e: getText(e) in regions)
                    rgnName = regions[ getText(metaGroupNode) ]
                else:
                    metaGroupNode = SeqUtils.expect_single(group_nodes)
                    rgnName = getText(metaGroupNode)
                    
                assert not id in cableIDToRegionName
                cableIDToRegionName[id] = rgnName
                
            else:
                cableIDToRegionName[id] = None
                pass
            
                 
            
            print "Loaded Cable: ", id, name
            
            
        # Load the segments:
        segmentListInfo = {} # id -> (id, name, cable,parent,(px,py,pz,pDiam),(dx,dy,dz,dDiam) )
        segmentsNode = SeqUtils.filter_expect_single(cellNode.childNodes, isElementWithTag("segments"))
        for segNode in Filter(segmentsNode.childNodes, isElementWithTag("segment")):
            print "Segment"
            id = segNode.getAttribute("id")
            name = segNode.getAttribute("name")
            cable = segNode.getAttribute("cable")
            parent = segNode.getAttribute("parent")
            
            # Every point should have a distal End:
            dNode = SeqUtils.filter_expect_single(segNode.childNodes, isElementWithTag("distal"))
            d_x, d_y, d_z = dNode.getAttribute("x"), dNode.getAttribute("y"), dNode.getAttribute("z")
            d_diam = dNode.getAttribute("diameter")
            
            
            
            if not parent:
                pass
                pNode = SeqUtils.filter_expect_single(segNode.childNodes, isElementWithTag("proximal"))
                p_x, p_y, p_z = pNode.getAttribute("x"), pNode.getAttribute("y"), pNode.getAttribute("z")
                p_diam = pNode.getAttribute("diameter")
                
            else:
                # Not every point need have a proximal end, we look at the parent in case it has
                # both and check the locations agree 
                parent_Dist_Loc = segmentListInfo[parent][5] 
                
                
                pNode = Filter(segNode.childNodes, isElementWithTag("proximal"))
                if len(pNode) == 0:
                    p_x, p_y, p_z, p_diam = parent_Dist_Loc
                    
                elif len(pNode) == 1:
                    p_xR, p_yR, p_zR = pNode[0].getAttribute("x"), pNode[0].getAttribute("y"), pNode[0].getAttribute("z")
                    p_diamR = pNode[0].getAttribute("diameter")
                    
                    # I do not understand MorphML to understand why these checks do not fail....
                    #print (p_xR,p_yR,p_zR) 
                    #print (parent_Dist_Loc[0],parent_Dist_Loc[1],parent_Dist_Loc[2] )
                    #assert (p_xR,p_yR,p_zR) == (parent_Dist_Loc[0],parent_Dist_Loc[1],parent_Dist_Loc[2] )
                    # In this case, use the diameter just read:
                    p_x, p_y, p_z = p_xR, p_yR, p_zR
                    p_diam = p_diamR
                    
                else:
                    assert False
            
            
            print id, name, cable, parent, (p_x, p_y, p_z, p_diam), (d_x, d_y, d_z, d_diam) 
            infTuple = (id, name, cable, parent, (float(p_x), float(p_y), float(p_z), float(p_diam)), (float(d_x), float(d_y), float(d_z), float(d_diam)))
            assert not id in segmentListInfo 
            segmentListInfo[id] = infTuple
    
    
        # Now we have read the file and created the dictionaries:
        return cableIDToRegionName, segmentListInfo



    
    
    
MorphologyImporter.register(method_name="fromMorphML", import_functor = MorphMLLoader.Load, as_type=MorphologyTree) 
        


