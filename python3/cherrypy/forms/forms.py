#! /usr/bin/env python3

import cherrypy


class Forms():
    @cherrypy.expose
    def index(self, username=None, password=None):

        if username is None or password is None:
            f = open("login_form.html")
            html = f.read()
        else:
            if username == "ptracton" and password == "ucla":
                html = """ <html> <head> LOGGED IN</head> <body>You have logged in</body>"""
            else:
                html = """ <html> <head> LOG IN FAIL</head> <body> <a href="/">HOME</a> </body>"""
        return html

if __name__ == '__main__':
    cherrypy.quickstart(Forms())
