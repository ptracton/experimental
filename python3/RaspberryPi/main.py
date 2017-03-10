#! /usr/bin/env python3
"""
File: main.py
Author: Phil Tracton

This is a test program to demonstrate a bottle web server running in
conjunction with threads for both SMS and Twitter
"""

#
# Imports go here
#
import os
import socket
import threading
import time
import queue
import bottle
import mako
import mako.template
import mako.lookup
from beaker.middleware import SessionMiddleware

#
# Global Variable
#

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

#
# Classes or functions go here
#


def get_ip_address():
    """
    Get the server IP address without using the /etc/hosts file
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip


def check_login(username=None, password=None):
    """
    Check username and password against database to see
    if user is authorized
    """
    if username == "ptracton" and password == "ucla":
        return True
    else:
        return False


@bottle.get('/')
def login():
    """
    Front page of the web site
    """
    template_dir = os.getcwd() + '/templates/'
    mako.lookup.TemplateLookup(directories=[template_dir])
    login_template = mako.template.Template(
        filename='templates/login_form.html')

    mysession = bottle.request.environ.get('beaker.session')
    print(mysession)

    if 'logged_in' not in mysession:
        mysession['logged_in'] = False
        mysession.save()
    
    if mysession['logged_in'] is True:
        username = mysession['username']
        remote_address = mysession['remote_address']
        return mako.template.Template(
            filename='templates/login_success_template.html').render(
                username=username, ip_address=remote_address, x=5)
    else:
        mysession['logged_in'] = False
        mysession.save()
        return login_template.render(address=get_ip_address())


@bottle.post('/')
def do_login():

    #
    # Read Cookies
    #
    visit_date_time = bottle.request.get_cookie("visit_date_time")
    remote_addr = bottle.request.get_cookie("remote_addr")
    remote_web_browser = bottle.request.get_cookie("remote_web_browser")

    #
    # Display Cookies
    #
    if visit_date_time:
        print("Last Visit: %s" % visit_date_time)
    if remote_addr:
        print("Last Remote Address %s" % remote_addr)
    if remote_web_browser:
        print("Last Remote Browser %s" % remote_web_browser)

    #
    # Get current data
    #
    current_time = time.strftime("%d/%m/%Y %H:%M:%S")
    remote_addr = bottle.request.environ.get('REMOTE_ADDR')
    remote_web_browser = bottle.request.environ.get('HTTP_USER_AGENT')
    print("Current Visit %s " % current_time)
    print("Current Remote Address %s" % remote_addr)
    print("Current Remote Web Browser %s" % remote_web_browser)

    #
    # Set Cookies
    #
    bottle.response.set_cookie("visit_date_time", current_time)
    bottle.response.set_cookie("remote_addr", remote_addr)
    bottle.response.set_cookie("remote_web_browser", remote_web_browser)

    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    remote_address = bottle.request.environ.get('REMOTE_ADDR')
    template_dir = os.getcwd() + '/templates/'
    mako.lookup.TemplateLookup(directories=[template_dir])
    print(remote_address)
    mysession = bottle.request.environ.get('beaker.session')
    if check_login(username, password):
        mysession['logged_in'] = True
        mysession['username'] = username
        mysession['remote_address'] = remote_address
        return mako.template.Template(
            filename='templates/login_success_template.html').render(
                username=username, ip_address=remote_address, x=5)
    else:
        mysession['logged_in'] = False
        return mako.template.Template(
            filename='templates/login_fail_template.html').render(
                username=username)


#
# Program starts running from here
#
if __name__ == "__main__":
    #
    # Instantiate classes and call functions from here
    #
    ip_address = get_ip_address()
    ip_address = "127.0.0.1"
    print("Running Server on IP Address %s" % ip_address)
#    bottle.run(app=app, host=ip_address, port=8080, debug=True,  reloader=True)


