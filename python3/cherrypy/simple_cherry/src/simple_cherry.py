'''
Created on Mar 29, 2013

@author: ptracton
'''
import cherrypy

class HelloWorld( object ):
    def index( self ):
        return "<b>Cherry Py Says Hello </b>World!"
    index.exposed = True

if __name__ == '__main__':
    cherrypy.quickstart( HelloWorld() )
