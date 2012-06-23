#
#
#
#
#import glob
#
#from os.path import join as Join
#from neurounits.importers.neuroml import ChannelMLReader, NeuroMLFileContainsNoChannels #parse_channelml_file
#
#
#
#
#subdirs = [
#    "CA1PyramidalCell_NeuroML",
#    "GranCellLayer_NeuroML",
#    "GranuleCell_NeuroML",
#    "MainenEtAl_PyramidalCell_NeuroML",
#    "SolinasEtAl_GolgiCell_NeuroML",
#    "Thalamocortical_NeuroML",
#    "VervaekeEtAl-GolgiCellNetwork_NeuroML",
#]
#
#simSrcDir = "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/"
#
#
#
#
#
#
#def get_chl_info_dir():
#    chlInfo = []
#
#
#
#    for subdir in subdirs:
#
#        for xmlfile in glob.glob( Join(simSrcDir, subdir) + '/*.xml'):
#
#            try:
#                ChannelMLReader.LoadChlRaw(xmlfile)
#                chlInfo.append(  xmlfile )
#            except NeuroMLFileContainsNoChannels,e:
#                pass
#            except:
#                raise
#
#
#    return chlInfo
