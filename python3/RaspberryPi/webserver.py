#! /usr/bin/env python3
"""
File: template_class.py
Author: YOUR NAME GOES HERE

This is an example template of how a python program should be structured.
It is a good starting point for any new coders.

You should change this comment to reflect what will be in the file
"""

#
# Imports go here
#
import os
import socket
import time
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


@bottle.route('/delete')
def delete_cookie():
    """
    Delete cookies and clean up session
    """

    bottle.response.delete_cookie(key="visited_date_time")
    bottle.response.delete_cookie(key="remote_addr")
    bottle.response.delete_cookie(key="remote_web_browser")

    mysession = bottle.request.environ.get('beaker.session')
    mysession['username'] = None
    mysession['remote_address'] = None
    mysession['logged_in'] = False
    mysession.save()

    html = 'Cookies deleted! <p>'
    html += '<a href = "/">Front</a>'
    return html


@bottle.get('/')
def login():
    """
    Front page of the web site
    """
    template_dir = os.getcwd() + '/templates/'
    mylookup = mako.lookup.TemplateLookup(directories=[template_dir])
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
    mylookup = mako.lookup.TemplateLookup(directories=[template_dir])    
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


if __name__ == "__main__":
    import logging
    import queue
    import threading
    import database

    try:
        os.remove("webserver_test.log")
        os.remove("test_webserver_thread.db")
    except:
        pass

    logging.basicConfig(filename="webserver_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    db_queue = queue.Queue()
    db = database.Database(database_queue=db_queue,
                           database_file_name="test_webserver_thread.db")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "webserver_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=.65)
    del(message_data)
    del(message)

    ip_address = get_ip_address()
    print("Running Server on IP Address %s" % ip_address)
    bottle.run(app=app, host=ip_address, port=8080, debug=True,  reloader=True)
