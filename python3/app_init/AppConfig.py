
import sys
import os
import ConfigTools

class AppConfig( ConfigTools.ConfigTools ):

    def __init__(self):
        super().__init__()
        print ("App Config")

        self.ConfigFile = None
        self.HomeDirectory = os.environ['HOME']
        self.ConfigDirectory = self.HomeDirectory+"/.app/"
        self.ConfigFile = self.ConfigDirectory +"app.ini"
        self.FileObject = None
        return

    def ConfigExists(self):
        """
        Returns a True if ~/.app/app.ini file exists.
        Returns a False otherwise
        """
        return os.path.exists(self.ConfigFile)

    def OpenFile(self):
        try:
            if not os.path.exists(self.ConfigDirectory):
                os.mkdir(self.ConfigDirectory)

            self.FileObject = open(self.ConfigFile, "w")
        except:
            return False

        return True

    def WriteFile(self):
        self.write(self.FileObject)

    def AddSectionAndData(self, section = None, option =None, data = None):
        if (not self.OpenFile()):
            sys.exit(1)

        if not (self.has_section(section)):   
            self.add_section(section)
            
        self.set(section, option, str(data))
