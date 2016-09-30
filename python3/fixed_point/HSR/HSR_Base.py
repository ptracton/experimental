#! /usr/bin/env python3

'''
'''

import re
import sys

class Vector:
    def __init__(self):
        self._file_name = None
        self._vector = []
        self.file_ready = False
        self._size = None
        self._c_file_name = None
        self._file_name_root = None
        return
    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, data=[]):
        self._vector = data
        return

    @property
    def size(self):
        return self._size

    @property
    def file_name_root(self):
        return self._file_name_root
        
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, name=None):
        self._file_name = name
        temp = name.split('/')
        self._file_name_root  = temp[-1].split('.')[0]
        self._c_file_name =  self._file_name_root+'.c'
        print (self._c_file_name)
        return
              
    def read_vector(self):
        """
        Read the filename and store results in the _vector
        """
        if self._file_name is None:
            return

        try:
            f = open(self._file_name)
            lines = f.readlines()
            f.close()
        except:
            print ("Failed to open or read %s" % self._file_name)
            sys.exit(-1)

        for line in lines:
            line_skip = re.search('//', line)
            if line_skip:
                next
            else:
                number = int(line, 16)
                if (number> 0x7FFF):
                    number= number - 0x10000
                self._vector.append(number)
        self._size = len(self._vector)

    def store_vector(self):
        '''
        Store this instance's vector as an array in C
        '''
        if self._file_name is None:
            return

        try:
            f = open(self._c_file_name, 'w')
        except:
            print ("Failed to open %s for writing" % self._file_name)
            sys.exit(-1)
            
        f.write("#include <stdint.h>\n");
        f.write("const int16_t %s[%d] = {\n"% (self._file_name_root, len(self._vector)))
        for x in range(len(self._vector)):
            f.write ('0x%04x,\n' % x)
        f.write("};\n\n");
        return
        
class HSR_Base:
    '''
    '''

    
    def __init__(self):
        '''
        '''
        self._vector1 = Vector()
        self._vector2 = Vector()
        self._result_vector = Vector()
        return

    @property
    def vector1(self):
        return self._vector1

    @property
    def vector2(self):
        return self._vector2
        
    @property
    def result_vector(self):
        return self._result_vector

    def saturate(self, number=None):
        if (number > 32767):
            number = 32767
        elif (number < -32768):
            number = -32768
            
        return number
        
    def calculate(self):
        '''
        OVERRIDE THIS METHOD!
        '''
        return
