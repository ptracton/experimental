import sys
import os
import configparser

class ToolOptions(object):
    def __init__(self):
        self.Executable = None
        self.FilesList = []
        self.OptionsList = []
        self.IncludePathList = []

class TechnologyOptions(object):
    def __init__(self):
        self.Netlist = None
        self.SDF = None
        self.Constraints = None
        self.FPGA = None
        self.BackEnd = ToolOptions()

class ConfigTools( configparser.SafeConfigParser ):

    def __init__(self):
        super(ConfigTools, self).__init__()
        return
