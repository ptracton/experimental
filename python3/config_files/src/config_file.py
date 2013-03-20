'''
Created on Dec 4, 2012

@author: ptracton
'''

import config_inherit
import config_instance

if __name__ == '__main__':

    inherit = config_inherit.config_inherit()
    instance = config_instance.config_instance()

    inherit.read( "project_config.ini" )
    instance.configparser.read( "project_config.ini" )

    print( "\nInheritance " )
    sections_list = inherit.sections()

    for x in sections_list:
        print ( x )
        items_list = inherit.items( x )
        print( "%s %s" % ( x, items_list ) )

    print( "\nInstance" )
    sections_list = instance.configparser.sections()
    print( sections_list )
    pass

