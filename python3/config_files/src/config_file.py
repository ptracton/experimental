'''
Created on Dec 4, 2012

@author: ptracton
'''

import config_inherit

if __name__ == '__main__':

    inherit = config_inherit.config_inherit()
    inherit.read( "project_config.ini" )
    sections_list = inherit.sections()
    for x in sections_list:
        print ( x )
        items_list = inherit.items( x )
        print( "%s %s" % ( x, items_list ) )
    pass

