#!  /usr/bin/env python3
'''
Created on Mar 29, 2013

@author: ptracton
'''
import cherrypy


class HelloWorld():
    """
    Simple Demo Class for CherryPy
    """
    @cherrypy.expose
    def index(self):
        """
        This is /
        """
        return """<b>Cherry Py Says Hello </b> World! <a href="link"> LINK</a> """

    @cherrypy.expose
    def link(self):
        return """We are at LINK, go <a href="/">HOME</a> """

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
