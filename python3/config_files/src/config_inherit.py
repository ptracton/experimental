'''
Created on Dec 4, 2012

@author: ptracton
'''

import configparser

class config_inherit( configparser.SafeConfigParser ):
    '''
    classdocs
    '''


    def __init__( self ):
        '''
        Constructor
        '''
        super().__init__()


if __name__ == '__main__':

    inherit = config_inherit()

    pass
