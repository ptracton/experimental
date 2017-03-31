#! /usr/bin/env python3

import os
import socket

import cherrypy
import mako
import mako.template
import mako.lookup


def get_ip_address():
    """
    Get the server IP address without using the /etc/hosts file
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip


class Templates():
    def checkLogin(self, username=None, password=None):
        return (username == "ptracton" and password == "ucla")

    @cherrypy.expose
    def index(self, username=None, password=None):

        remote_address = get_ip_address()
        template_dir = os.getcwd() + '/templates/'
        mako.lookup.TemplateLookup(directories=[template_dir])
        login_template = mako.template.Template(
            filename='templates/login_form.html')

        if username is None and password is None:
            html = login_template.render(address=get_ip_address())
        elif self.checkLogin(username, password):
            html = mako.template.Template(
                filename='templates/login_success_template.html').render(
                    username=username, ip_address=remote_address, x=5)
        else:
            html = mako.template.Template(
                filename='templates/login_fail_template.html').render(
                    username=username)
        return html


if __name__ == "__main__":
    cherrypy.quickstart(Templates())
