
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



import mreorg
from morphforge.core.mgrs.locmgr import LocMgr


root = os.path.normpath( os.path.join( LocMgr.get_root_path(), "..") )
examples_src_dir = os.path.join(root, "src/morphforgeexamples/")


#"/home/michael/hw/morphforge/doc"
doc_src_dir = os.path.normpath( os.path.join(root, "doc") )

examples_dst_dir =  os.path.join(root, "doc/srcs_generated_examples")
examples_dst_dir_images =  os.path.join(root, "doc/srcs_generated_examples/images/")

examples_build_dir = os.path.join( LocMgr.get_tmp_path(), "mf_doc_build")
examples_build_dir_image_out = os.path.join( examples_build_dir,  "images/")


dirs = ['morphology', 'singlecell_simulation', 'multicell_simulation', 'advanced_examples']#, 'assorted' ]
example_subdirs = [ d for d in os.listdir(examples_src_dir) if d.startswith("""exset""") ]
dirs = sorted(example_subdirs)

example_srcs = list( itertools.chain( *[ sorted(Glob( Join(examples_src_dir, dir) + "/*.py") ) for dir in dirs] ) )




def clear_directory(d):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)




def parse_src_file(filename, docstring):
    d = open(filename, 'r').read()

    # Remove copyright notice:
    d = re.split("""[#]\s?[-]+""", d)[-1]

    # Remove the docstring:
    if docstring is not None:
        raw_docstring = r'''"""\s*%s\s*"""''' % re.escape(docstring).strip()
        d = re.sub(raw_docstring, '', d, re.MULTILINE)

    return d



rstTmpl = """
$title
$titleunderline


$docstring

Code
~~~~

.. code-block:: python

$code




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




Output
~~~~~~

.. code-block:: bash

    $output




"""

def make_rst_output(index, examples_filename, src_code, output_images, docstring, output):
    name_short = os.path.split(examples_filename)[1]
    name_short = os.path.splitext(name_short)[0]


    # Copy the image files accross:
    im_names = []
    for im in output_images:
        im_newName = os.path.join(examples_dst_dir_images, "%s_%s"%(name_short, os.path.split(im)[-1]))
        shutil.copyfile(im, im_newName)

        im_newName_short = im_newName.replace(doc_src_dir, "") #/home/michael/hw/morphforge/doc", "")
        im_names.append(im_newName_short)

    title =  [ l.strip() for l in docstring.split(".")[0].split("\n") if l.strip() ] [0] if docstring else None

    title = title or '<Missing Docstring>'


    # Clean up the output (especially the '\r's iduring simulation
    output = output.strip()
    output = '\n'.join( [ l for l in output.split('\n') if not '\r' in l] )

    # Prefix the title:
    title = "%d. "%(index+1) +title
    # Create the rst:
    context = {
                'title':title,
                'titleunderline':"="*len(title),
                'docstring': docstring,
                'code' : "\n".join( ["    "+l for l in src_code.split("\n")] ),
                'figures':im_names,
                'output' : "\n".join( ["    "+l for l in output.split("\n")] ),
                }
    s = Template(rstTmpl, context).respond()

    op_rst_filename = os.path.join( examples_dst_dir, name_short+".rst")
    with open(op_rst_filename, 'w') as fOut:
        fOut.write(s)





saveCodeTmpl = """
import matplotlib
import pylab
for fig_num, fig_mgr in matplotlib._pylab_helpers.Gcf.figs.iteritems():
    matplotlib._pylab_helpers.Gcf.set_active(fig_mgr)
    pylab.savefig("{{OUTDIR}}out%d.png" % fig_num, facecolor='lightgrey')
"""

def run_example(index, filename):
    print 'Running Example:', filename
    newFilename = os.path.join( examples_build_dir, os.path.split(filename)[1] )

    # Clear the directory
    clear_directory(examples_build_dir)
    clear_directory(examples_build_dir_image_out)

    #Create the python file to run:
    with open(newFilename, 'w') as fOut:
            fOut.write( open(filename).read() )
            saveCode = saveCodeTmpl.replace("{{OUTDIR}}", examples_build_dir_image_out)
            fOut.write(saveCode)



    # run the file, and capture the output:

    # Turn off plotting:
    env = os.environ.copy()
    env['MREORG_CONFIG'] = "BATCHRUN"

    args = shlex.split("""python %s"""%newFilename)

    try:
        result = subprocess.check_output(args, stderr=subprocess.STDOUT, env=env)
    except subprocess.CalledProcessError:
        print '  ** Error Running file'
        result = ''

    # Split the output to get at the docstring:
    docstring = mreorg.utils.extract_docstring_from_fileobj( open(filename))

    # Get the images:
    images = glob.glob(examples_build_dir_image_out + "/*")

    # Clean up the source code:
    src_code = parse_src_file(filename, docstring)

    # Create the Output RST File:
    make_rst_output( index=index, examples_filename=filename, src_code=src_code, output_images=images, docstring=docstring, output=result)




# Start with an empty directory:
clear_directory(examples_dst_dir)
clear_directory(examples_dst_dir_images)

for index, fName in enumerate(example_srcs):
    fName_full = os.path.join(examples_src_dir, fName)
    run_example(index, fName_full)

