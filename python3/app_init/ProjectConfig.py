import sys
import os
import configparser

class TechnologyOptions(object):
    def __init__(self):
        self.Netlist = None
        self.SDF = None
        self.Constraints = None
        self.FPGA = None
        self.SynthesisOptions = []
        self.SynthesisFilesList = []

class SimulationOptions(object):
    def __init__(self):
        self.SimulationFilesList = []
        self.SimulationOptionsList = []
        self.SimulationIncludePathList = []

class ProjectConfig( configparser.SafeConfigParser ):

    def __init__(self):
        super().__init__()
        print ("Project Config")

        self.FileObject = None
        self.FileName = None
        ##
        ## Top Level Project Settings
        ## 
        self.ProjectName = None
        self.TestBench = None
        self.TestBenchInstance = None
        self.TopLevel = None
        self.CPU = None

        ##
        ## Project Specific
        ##
        self.ProjectSimulation = SimulationOptions()

        ##
        ## Cores that we are using
        ## 
        self.CoreList = []
        self.CoresSimulation = SimulationOptions()

        ##
        ## Xilinx Specific
        ##
        self.Xilinx = TechnologyOptions()

        ##
        ## Altera Specific
        ##
        self.Altera = TechnologyOptions()

        ##
        ## ASIC Specific
        ##
        self.ASIC = TechnologyOptions()

        return

    def ConfigExists(self, path):
        """
        Returns a True if path exists
        Returns a False otherwise
        """
        self.FileName =path
        return os.path.exists(path)

    def OpenFile(self, ConfigFile):
        try:
            self.FileObject = open(ConfigFile, "w")
        except:
            return False

        return True

    def WriteFile(self):        
        self.write(self.FileObject)

    def AddSectionAndData(self, section = None, option =None, data = None):
        if (not self.OpenFile(self.FileName)):
            sys.exit(1)
        print ("Section %s Option %s Data %s" % (section, option, str(data)))
        if not (self.has_section(section)):   
            self.add_section(section)
            
        self.set(section, option, str(data))
