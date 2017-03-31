#! /usr/bin/env python3

import cherrypy


class MyCookieApp(object):
    @cherrypy.expose
    def set(self):
        cookie = cherrypy.response.cookie
        cookie['cookieName'] = 'cookieValue'
        cookie['cookieName']['path'] = '/'
        cookie['cookieName']['max-age'] = 3600
        cookie['cookieName']['version'] = 1
        return "<html><body>Hello, I just sent you a cookie</body></html>"

    @cherrypy.expose
    def read(self):
        cookie = cherrypy.request.cookie
        res = """<html><body>Hi, you sent me %s cookies.<br />
                Here is a list of cookie names/values:<br />""" % len(cookie)
        for name in cookie.keys():
            res += "name: %s, value: %s<br>" % (name, cookie[name].value)
        return res + "</body></html>"

if __name__ == '__main__':
    #http://127.0.0.1:8080/cookie/read
    #http://127.0.0.1:8080/cookie/set
    cherrypy.quickstart(MyCookieApp(), '/cookie')
