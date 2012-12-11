'''
Created on Dec 4, 2012

@author: ptracton
'''

import configparser

class config_instance( object ):
    '''
    classdocs
    '''


    def __init__( self ):
        '''
        Constructor
        '''
        self.configparser = configparser.SafeConfigParser()


if __name__ == '__main__':

    instance = config_instance()

    pass
