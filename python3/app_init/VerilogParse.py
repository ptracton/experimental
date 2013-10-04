#! /usr/bin/env python3

import sys
import re

class VerilogStrings(object):
    def __init__(self, string = None):
        self.String = string

    def __strip_comments(self, s):
        x = re.search('(.*)\/\*.*\*\/', s)
        if (x):
            return True, x.group(1).lstrip()
        else:
            return False, s

    def __strip_output(self, s):
        x = re.search('output (.*)', s, re.IGNORECASE)
        y = re.search('OUTPUT (.*)', s, re.IGNORECASE)
        if (x):
            return True, x.group(1).lstrip()
        elif (y):
            return True, y.group(1).lstrip()
        else:
            return False,         

    def __strip_input(self, s):
        x = re.search('input (.*)', s, re.IGNORECASE)
        y = re.search('INPUT (.*)', s, re.IGNORECASE)
        if (x):
            return True, x.group(1).lstrip()
        elif (y):
            return True, y.group(1).lstrip()
        else:
            return False, s

    def __strip_wire (self, s):
        x = re.search('wire (.*)', s, re.IGNORECASE)
        y = re.search('WIRE (.*)', s, re.IGNORECASE)
        if (x):
            return True, x.group(1).lstrip()
        elif (y):
            return True, y.group(1).lstrip()
        else:
            return False, s
        return 

    def __strip_width(self, s):
        x = re.search('\[.*\] (.*)', s, re.IGNORECASE)
        if (x):
            return True, x.group(1).lstrip()
        else:
            return False, s
        return         

class Port(VerilogStrings):
    def __init__(self, string = None, direction = "Input", name = None, width = 1, start = 0, end = 0):
        super(Port, self).__init__(string = string)
        self.Direction = direction
        self.Name = name
        self.Width = width
        self.StartIndex = start
        self.EndIndex = end

    def ParsePort(self):
        state_comment, string_comment = self.__strip_comments(self.String)
        print ("Comment String: ", string_comment)
        return

    def __str__(self):
        str = "Port: "+self.Name+" Direction: " +self.Direction
        return str

class Parameter(object):
    def __init__(self, name = None, value = None):
        self.Name = name
        self.Value = value

class VerilogParse(object):
    """
    """

    def __init__(self, FileName = None):
        """
        """
        self.FileName = FileName
        self.InputPortsList = []
        self.OutputPortsList = []
        self.BidirectionalPortsList = []
        self.UknownPortsList = []
        self.ModulesList = []
        return
    
    def GetPorts(self):
        """
        """
        try:
            f = open(self.FileName, "r")
            lines = f.readlines()
            f.close()
        except:
            print("Failed to open or read %s" % (self.FileName))
            sys.exit(1)
            
        found_input = False
        found_output = False
        found_bidirectional = False
        found_module = False
        
        for line in lines:
            found_input = False
            found_output = False
            found_bidirectional = False
            #print(line)

            if (found_module):

                start_port = re.search('\W+(.*)', line)
                if (start_port):
                    if (len(start_port.group(1)) > 0):
                        #print ("Port %s" % (start_port.group(1)))
                        x = Port(string = start_port.group(1))
                        x.ParsePort()
                        self.UknownPortsList.append(x)
                        del(x)

                end_module = re.search('\);', line)
                if (end_module):
                    print("End Module")
                    found_module = False

            module_search = re.search('^module (.*)', line)
            if (module_search):
                module_name = ''.join(e for e in module_search.group(1) if e.isalnum())
                found_module = True
                print ("Module Name: ", module_name)


      

        print ("Unknown Ports " ,  self.InputPortsList)
        print ("Input Ports " ,  self.InputPortsList)
        print ("Ouptut Ports " ,  self.InputPortsList)

if __name__ == '__main__':
    
    v = VerilogParse(FileName = sys.argv[1])
    v.GetPorts()
    
    pass
