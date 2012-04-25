#! /usr/bin/python

import os
import sys
import glob



files = glob.glob( sys.argv[1] )


ext_gen = None

intermediate_filename_tmpl = "mf_tmpF%03d%s" 
op_file = "test1.avi"

os.system("rm mf_tmpF*")

for i,f in enumerate( sorted(files)):
    print i,f
    ext = os.path.splitext(f)[1]
    
    if ext_gen and ext != ext_gen:
        assert False, 'Inconsistent image file types! (%s, %s)'%( ext_gen, ext)
        ext_gen = ext
    
    
    new_name = intermediate_filename_tmpl%(i,ext)
    
    
    os.system('ln -s "%s" "%s" '%( f,new_name) )
    
if os.path.exists(op_file):
    os.unlink(op_file)
    

vid_cmd = "ffmpeg -r 1 -i mf_tmpF%03d.png -vcodec mpeg4 -r 24 test1.avi"
os.system(vid_cmd)




#ffmpeg -i test_%d.jpg -vcodec mpeg4 test.avi
#
