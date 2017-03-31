#! /usr/bin/env python3


import cherrypy


class Sessions():

    @cherrypy.expose
    def index(self):
        if 'count' not in cherrypy.session:
            cherrypy.session['count'] = 0
        cherrypy.session['count'] += 1
        #print(cherrypy.session['count'])
        #print(cherrypy.session.id)
        return """ {} """.format(cherrypy.session['count'])


if __name__ == "__main__":
    cherrypy.config.update({'tools.sessions.on': True,
                            'tools.sessions.timeout': 10
                        })
    cherrypy.config.update({'server.socket_port': 5000})
    cherrypy.quickstart(Sessions())
