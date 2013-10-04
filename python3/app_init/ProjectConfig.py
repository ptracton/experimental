import sys
import os
import configparser
import ConfigTools


class ProjectConfig( ConfigTools.ConfigTools ):

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
        self.ProjectSimulation = ConfigTools.ToolOptions()

        ##
        ## Cores that we are using
        ## 
        self.CoreList = []
        self.CoresSimulation = ConfigTools.ToolOptions()

        ##
        ## Xilinx Specific
        ##
        self.Xilinx = ConfigTools.TechnologyOptions()

        ##
        ## Altera Specific
        ##
        self.Altera = ConfigTools.TechnologyOptions()

        ##
        ## ASIC Specific
        ##
        self.ASIC = ConfigTools.TechnologyOptions()

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
