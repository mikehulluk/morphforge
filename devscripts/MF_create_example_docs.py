
import os
import shutil
import shlex
import subprocess
import glob
import re
import itertools
from glob import glob as Glob
from os.path import join as Join

from Cheetah.Template import Template


 
from morphforge.core.mgrs.locmgr import LocMgr


root = os.path.normpath( os.path.join( LocMgr.getRootPath(), "..") )
examples_src_dir = os.path.join(root, "src/morphforgeexamples/")
examples_dst_dir =  os.path.join(root, "doc/srcs_generated_examples")
examples_dst_dir_images =  os.path.join(root, "doc/srcs_generated_examples/images/")

examples_build_dir = os.path.join( LocMgr.getTmpPath(), "mf_doc_build")
examples_build_dir_image_out = os.path.join( examples_build_dir,"images/")

dirs = ['morphology','singlecell_simulation','multicell_simulation', 'advanced_examples', 'assorted' ]
example_srcs = list( itertools.chain( *[ Glob( Join(examples_src_dir, dir) + "/*.py") for dir in dirs] ) )  
                                     



def clear_directory(d):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)




def parse_src_file(filename, docstring):
    d = open(filename,'r').read()
    
    # Remove copyright notice:
    d = re.split("""[#][-]+""", d)[-1]

    # Remove the docstring:
    raw_docstring = r'''"""\s*%s\s*"""'''%  re.escape(docstring).strip()
    d = re.sub(raw_docstring,'', d, re.MULTILINE)

    return d



rstTmpl = """
$title
$titleunderline


$docstring

Code
~~~~

.. code-block:: python

$code


Output
~~~~~~

.. code-block:: bash

    $output



#if $figures
Figures
~~~~~~~~

#for $im in $figures

.. figure:: $im
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure <$im>`

#end for

#end if

"""

def make_rst_output(index, examples_filename, src_code, output_images, docstring, output):
    name_short = os.path.split(examples_filename)[1]
    name_short = os.path.splitext(name_short)[0]


    # Copy the image files accross:
    im_names = []
    for im in output_images:
        im_newName = os.path.join(examples_dst_dir_images, "%s_%s"%(name_short, os.path.split(im)[-1]))
        shutil.copyfile(im, im_newName)

        im_newName_short = im_newName.replace("/home/michael/hw/morphforge/doc","")
        im_names.append(im_newName_short)

    title = "%d. "%(index+1) + [ l.strip() for l in docstring.split(".")[0].split("\n") if l.strip() ] [0]
    title = title or 'Missing Docstring'

    # Create the rst:
    context = {
                'title':title,
                'titleunderline':"="*len(title),
                'docstring': docstring,
                'code' : "\n".join( ["\t"+l for l in src_code.split("\n")] ),
                'figures':im_names,
                'output' : "\n".join( ["\t"+l for l in output.split("\n")] ),
                }
    s = Template(rstTmpl, context).respond()

    op_rst_filename = os.path.join( examples_dst_dir, name_short+".rst")
    with open(op_rst_filename,'w') as fOut:
        fOut.write(s)





saveCodeTmpl = """
import matplotlib
import pylab
for fig_num,fig_mgr in matplotlib._pylab_helpers.Gcf.figs.iteritems():
    matplotlib._pylab_helpers.Gcf.set_active(fig_mgr)
    pylab.savefig("{{OUTDIR}}out%d.png"%fig_num, facecolor='lightgrey')
print "DOCSTRING:"
print globals()['__doc__']
"""

def run_example(index,filename):
    print 'Running Example:', filename
    newFilename = os.path.join( examples_build_dir, os.path.split(filename)[1] )

    # Clear the directory
    clear_directory(examples_build_dir)
    clear_directory(examples_build_dir_image_out)

    #Create the python file to run:
    with open(newFilename,'w') as fOut:
            fOut.write( open(filename).read() )
            saveCode = saveCodeTmpl.replace("{{OUTDIR}}",examples_build_dir_image_out)
            fOut.write(saveCode)


    
    # Run the file, and capture the output:
    
    # Turn off plotting:
    env = os.environ.copy()
    env['MF_PLOT'] = 'OFF'
    
    cmd = """python %s"""%newFilename
    args = shlex.split(cmd)
    process = subprocess.Popen(args, stdout=subprocess.PIPE,env=env)
    result = process.communicate()[0]


    # Split the output to get at the docstring:
    print result
    output, docstring = result.split("DOCSTRING:")

    # Get the images:
    images = glob.glob(examples_build_dir_image_out + "/*")

    # Clean up the source code:
    src_code = parse_src_file(filename,docstring)

    # Create the Output RST File:
    make_rst_output( index=index,examples_filename=filename, src_code=src_code, output_images=images, docstring=docstring, output=output)




# Start with an empty directory:
clear_directory(examples_dst_dir)
clear_directory(examples_dst_dir_images)

for index,fName in enumerate(example_srcs):
    fName_full = os.path.join(examples_src_dir,fName)
    run_example(index,fName_full)
    #clear_directory(examples_build_dir)

