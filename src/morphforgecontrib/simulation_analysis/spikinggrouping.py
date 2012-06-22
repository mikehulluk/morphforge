




import numpy as np
from morphforge.traces.eventset import EventSet
 

class DBScan(object):
    
    
    @classmethod
    def query_region(cls, p, eps, pts):
        nr_indices = np.nonzero( np.fabs(pts-p) < eps)[0]
        #print nr_indices
        return set( nr_indices )
    
    
    @classmethod
    def run(cls, pts, eps, min_pts ):
        pts = np.array(pts)
        visited_indices = [False] * np.zeros( len(pts) )
        noise = [] 
        clusters = []
        
        for i,pt in enumerate(pts):
            if visited_indices[i]:
                continue
            
            visited_indices[i] = 1
            
            N = cls.query_region(p=pt, eps=eps, pts=pts)
            
            if len(N) < min_pts:
                noise.append(i)
            else:
                C = set()
                cls.expandCluster(pt_index=i, N=N, C=C, eps=eps, pts=pts, minPts=min_pts,  visited_indices=visited_indices, clusters=clusters) 
                clusters.append(C)
        
        return clusters, noise
            
            
    @classmethod
    def expandCluster(cls, pt_index, N, C, pts, eps, visited_indices,  minPts, clusters):

        C.add(pt_index)
        
        iter_N = list( N )
        while iter_N:
            pdash_index = iter_N.pop()
            if not visited_indices[pdash_index]:
                
                visited_indices[pdash_index] = 1
                N_dash = cls.query_region(p=pts[pdash_index], eps=eps, pts=pts)
                
                if len(N_dash) >= minPts:
                    for n in N_dash:
                        iter_N.append(n)
                
                pt_in_clusters = [ True for c in clusters if pdash_index in c]
                if not pt_in_clusters:
                    C.add(pdash_index)            
                         
            
    @classmethod            
    def cluster_spike_times(cls, event_set, eps, min_pts=5):
        eps=float( eps.rescale("ms").magnitude )        
        

        data = [ float( ev.get_time().rescale("ms") ) for ev in event_set ]            
        clusters, noise = DBScan.run( pts = np.array(data), eps=eps, min_pts=min_pts)
        
        # Create new eventsets for each cluster
        new_eventsets = []
        for cluster in clusters:
            e = EventSet()
            for c in cluster:
                e.add_event( event_set[c] )
            new_eventsets.append(e)
        
        # Create a new EventSet for the noise points:
        noise_event_set = EventSet(events= [event_set[i] for i in noise] )

        return new_eventsets, noise_event_set


    @classmethod
    def calculate_mean_frequency(cls, cluster_sets):
        
        
        mean_times = [ np.mean( [t.rescale("ms") for t in c.times]) for c in cluster_sets if len(c) != 0 ]
        mean_times = np.array( [ mt for mt in mean_times if mt > 200 ] )
         
        np.sort( mean_times )
        mean_times.sort()
        print mean_times
        
        isi = np.diff(mean_times)
        freq = 1000.0 / isi
        #pylab.hist(freq)
        mean_freq = np.mean( freq)

        return mean_freq
    
     
#DBSCAN(D, eps, MinPts)
#   C = 0
#   for each unvisited point P in dataset D
#      mark P as visited
#      N = regionQuery(P, eps)
#      if sizeof(N) < MinPts
#         mark P as NOISE
#      else
#         C = next cluster
#         expandCluster(P, N, C, eps, MinPts)
#          
#expandCluster(P, N, C, eps, MinPts)
#   add P to cluster C
#   for each point P' in N 
#      if P' is not visited
#         mark P' as visited
#         N' = regionQuery(P', eps)
#         if sizeof(N') >= MinPts
#            N = N joined with N'
#      if P' is not yet member of any cluster
#         add P' to cluster C




#
#with open("/home/michael/Desktop/save_spikes.txt") as fIn:
#    data = fIn.read().split()
#
#
#
#data = np.array( [ float(s) for s in data] )
##data.sort()
##data = data[0:50]
#
#clusters, noise = DBScan.run( pts = data, eps=5, min_pts=5)
#
#for c in clusters:
#    print 'Cluster:', c
#    #print c
#
#import pylab
#colors = ['rgbykrgbykrgbykrgbykrgbykrgbykrgbykrgbyk']
#for i,c in enumerate(clusters):
#    indices = np.array( list(c) )
#    print indices
#    print data
#    d = data[ indices ]
#    pylab.scatter( d, [i]*len(d), colors[i]   ) 
#pylab.show()
