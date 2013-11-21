import sys
import os
import ConfigTools

class IPFile(object):
    def __init__(self, FileName = None):
        self.FileName = FileName
        self.InputPortList = []
        self.OutputPortList = []
        self.BidirectionalPortList = []
        self.ParameterList = []
        return

class IPConfig( ConfigTools.ConfigTools ):

    def __init__(self):
        super(IPConfig, self).__init__()
        print ("IP Config")
        
        self.Simlation = ConfigTools.ToolOptions()

        return
