#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are 
# met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
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


from morphforge.simulation.neuron.biophysics.mm_neuron import MM_Neuron_Base
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforge.simulation.core.biophysics.membranemechanism import MembraneMechanism
from neurounits.tools.nmodl import WriteToNMODL, MechanismType
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.membranemechanisms.common.neuron import build_HOC_default
from neurounits.neurounitparser import NeuroUnitParser
from morphforge.core import ObjectLabeller



class RecordableData(object):
    def __init__(self, standard_tags=None):
        self.standard_tags = standard_tags or []



class MM_Neuron_RecGen(NeuronRecordableOnLocation):
    def __init__(self, srcChl, modvar,unit_in_nrn, std_tags, **kwargs):
        super( MM_Neuron_RecGen, self).__init__(**kwargs)
        self.srcChl = srcChl
        self.modvar=modvar
        self.unit_in_nrn = unit_in_nrn
        self.std_tags = std_tags or []

    def buildMOD(self, modFileSet):
        pass

    def buildHOC(self, hocFile):
        HocModUtils.CreateRecordFromModFile( hocFile,
                                             vecname="RecVec%s"%self.name,
                                             celllocation=self.where,
                                             modvariable=self.modvar,
                                             mod_neuronsuffix=self.srcChl.NRNSUFFIX,
                                             recordobj=self)

    def getDescription(self):
        return "%s %s %s" % (self.modvar, self.srcChl.name, self.where.getLocationDescriptionStr() )

    def getUnit(self):
        return self.unit_in_nrn
    def getStdTags(self):
        return self.std_tags






class NeuroUnitEqnsetMechanism(MembraneMechanism):
    def __init__(self, eqnset ,mechanism_id, name=None,  default_parameters={}, recordables_map= None, recordables_data=None):
        MembraneMechanism.__init__(self, mechanism_id=mechanism_id)

        if isinstance( eqnset, basestring):
            eqnset = NeuroUnitParser.EqnSet(eqnset)

        self.name = name if name is not None else ObjectLabeller.getNextUnamedObjectName( NeuroUnitEqnsetMechanism)
        self._parameters = default_parameters
        self.eqnset = eqnset
        self.recordables_map = recordables_map or {}
        self.recordables_data =recordables_data or {}

        for param in eqnset.parameters:
            print'CHECKING'
            print param
            print param.symbol
            print 'iii', param.get_dimension().as_quantities_unit(), type(param.get_dimension().as_quantities_unit())
            print "iiii",default_parameters[param.symbol], type( default_parameters[param.symbol])
            assert param.symbol in default_parameters
            assert (param.get_dimension().as_quantities_unit() / default_parameters[param.symbol] ).rescale("")
            print 'OK\n'

    def getDefaults(self):
        return self._parameters

    def getVariables(self):
        return self._parameters.keys()



class Neuron_NeuroUnitEqnsetMechanism( MM_Neuron_Base, NeuroUnitEqnsetMechanism):
    def __init__(self, **kwargs):
        MM_Neuron_Base.__init__(self)
        NeuroUnitEqnsetMechanism.__init__(self, **kwargs)

        self.nmodl_txt, self.buildparameters = WriteToNMODL(self.eqnset, neuron_suffix="NRNEQNSET"+ObjectLabeller.getNextUnamedObjectName(Neuron_NeuroUnitEqnsetMechanism,prefix="" ))




        assert self.buildparameters.mechanismtype == MechanismType.Distributed
        self.units = {}
        for param_str, value in self._parameters.iteritems():
            sym = self.eqnset.get_terminal_obj(param_str)
            param_default_unit = self.buildparameters.symbol_units[sym]
            self.units[param_str] = param_default_unit.as_quantities_unit()

        self.NRNSUFFIX = self.buildparameters.suffix

    def build_HOC_Section( self, cell, section, hocFile, mta ):
        build_HOC_default( cell=cell, section=section, hocFile=hocFile, mta=mta , units=self.units, nrnsuffix=self.buildparameters.suffix )

    def createModFile(self, modFileSet):
        modFileSet.append(ModFile(name=self.name, modtxt=self.nmodl_txt ))


    def getModFileChangeables(self):
        change_attrs = set(['name',"nmodl_txt", 'mechanism_id',  'recordables_map', 'buildparameters', 'units', 'recordables_data'])
        fixed_attrs = set( ['mm_neuronNumber','cachedNeuronSuffix','eqnset','_parameters',] )
        print set( self.__dict__)
        assert set( self.__dict__) == fixed_attrs | change_attrs
        return dict ( [ (a, getattr(self, a)) for a in change_attrs ] )




    def getRecordables(self):
        return  self._getRecordableSymbols()
        assert False


    def _getRecordableSymbols(self):
        return [ s.symbol for s in list(self.eqnset.states) + list(self.eqnset.assignedvalues) + list(self.eqnset.suppliedvalues) + list(self.eqnset.parameters) ]

    def getRecordable(self, what, celllocation, **kwargs):

        # Map it through the recordables_map, so that we can alias to StandardTags:
        what = self.recordables_map.get(what,what)

        valid_symbols = self._getRecordableSymbols()
        if not what in  valid_symbols:
            err ="Unknown record value: %s. Expecting one of: %s "%(what, valid_symbols)
            raise ValueError(err)

        obj = self.eqnset.get_terminal_obj( what )
        unit_in_nrn = self.buildparameters.symbol_units[obj].as_quantities_unit()

        std_tags = []
        if what in self.recordables_data:
            std_tags = self.recordables_data[what].standard_tags

        return MM_Neuron_RecGen( srcChl=self, modvar=what, where=celllocation, unit_in_nrn=unit_in_nrn, std_tags=std_tags, **kwargs)



NeuronSimulationEnvironment.membranemechanisms.registerPlugin( NeuroUnitEqnsetMechanism, Neuron_NeuroUnitEqnsetMechanism)
