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
import configparser
import logging
import os
import queue
import socket
import sys
import threading
import time
import bottle
import mako
import mako.template
import mako.lookup
from beaker.middleware import SessionMiddleware
import cherrypy
import tornado
import twilio
from twilio import twiml
import twilio.rest

import database
import twitter

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

# copy in your Twilio Account SID and Auth Token from Twilio Console
config_file = "/home/ptracton/.ucla.cfg",
config = configparser.RawConfigParser()
config.read(config_file)
account_sid = config.get("TWILIO", "SID")
auth_token = config.get("TWILIO", "TOKEN")
TwilioClient = twilio.rest.TwilioRestClient(account_sid, auth_token)

#
# Database and Queue global variables for use in bottle application
#
db_queue = queue.Queue()
db = database.Database(database_queue=db_queue,
                       database_file_name="test_webserver_thread.db")

response_queue = queue.Queue()


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
    print("check_login: username=%s password=%s" % (username, password))
    cl_response_queue = queue.Queue()
    message_data = database.DatabaseDataMessage(
        table_name="webserver",
        field=""" "{}" """.format("WEBSERVER_USER_NAME"),
        data=""" "{}" """.format(username),
        caller_queue=cl_response_queue)
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_SELECT_DATA,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=0.65)

    print("check_login: Wait on password response")
    while cl_response_queue.empty() is True:
        pass

    print("check_login: Got password response")
    user_response = cl_response_queue.get()
    print(user_response)

    # Make sure there is some sort of response before
    # parsing it.
    if len(user_response):
        db_username = user_response[0][1]
        db_password = user_response[0][2]
        print("DB Username = %s" % (db_username))
        print("DB Password = %s" % (db_password))
        return (db_username == username and db_password == password)
    else:
        # There was no response so no chance of logging in or parsing
        # the response
        return False


@bottle.post('/twilio')
def inbound_sms():
    twiml_response = twiml.Response()
    # obtain message body from the request. could also get the "To" and
    # "From" phone numbers as well from parameters with those names
    inbound_message = bottle.request.forms.get("Body")
    response_message = "I don't understand what you meant...need more code!"
    # we can use the incoming message text in a condition statement
    if inbound_message == "Hello":
        response_message = "Well, hello right back at ya!"
    twiml_response.message(response_message)
    # we return back the mimetype because Twilio needs an XML response
    bottle.response.content_type = "application/xml"
    return str(twiml_response)


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


if __name__ == "__main__":
    try:
        os.remove("webserver_test.log")
        os.remove("test_webserver_thread.db")
    except:
        pass

    print("Starting Logging")
    logging.basicConfig(filename="webserver_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    print("Creating and Starting DB Thread")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    # print("Creating Twitter Thread")
    # twitter_queue = queue.Queue()
    # twitter_task = twitter.TwitterThread(config_file=config_file,
    #                                      response_queue=response_queue,
    #                                      db_queue=db_queue)
    # twitter_thread = threading.Thread(target=twitter_task.run, daemon=True)
    # twitter_thread.start()

    print("Creating Database")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "webserver_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    # print("Create SMS Table")
    # message_data = database.DatabaseDataMessage()
    # message_data.schema_file = "sms_table.sql"
    # message = database.DatabaseMessage(
    #     command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
    #     message=message_data)
    # db_queue.put(message)

    # print("Create Twitter Table")
    # message_data = database.DatabaseDataMessage()
    # message_data.schema_file = "twitter_table.sql"
    # message = database.DatabaseMessage(
    #     command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
    #     message=message_data)
    # db_queue.put(message)

    print("Run bottle")
    try:
        bottle.run(app=app, host="127.0.0.1", port=8080,
                   server="cherrypy",
                   debug=True,
                   reloader=True)
    except KeyboardInterrupt:
        db.kill()
        os.system("killall python3")
        sys.exit(0)
