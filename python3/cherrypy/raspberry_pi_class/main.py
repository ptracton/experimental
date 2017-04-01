#! /usr/bin/env python3

"""
DEFAULT LIBRARIES
"""
import configparser
import os
import queue
import socket
import threading

"""
THIRD PARTY LIBRARIES
"""
import cherrypy
import mako
import mako.template
import mako.lookup
import twilio
from twilio import twiml
import twilio.rest

"""
LOCAL LIBRARIES
"""
import database
import twitter

"""
GLOBALS
"""
db_queue = queue.Queue()
db = database.Database(database_queue=db_queue,
                       database_file_name="test_webserver_thread.db")

response_queue = queue.Queue()

# copy in your Twilio Account SID and Auth Token from Twilio Console
config_file = "/home/ptracton/.ucla.cfg",
config = configparser.RawConfigParser()
config.read(config_file)
account_sid = config.get("TWILIO", "SID")
auth_token = config.get("TWILIO", "TOKEN")
TwilioClient = twilio.rest.TwilioRestClient(account_sid, auth_token)


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


class Root(object):
    """
    Our cherrypy webserver
    """
    @cherrypy.expose
    def logout(self):
        address = get_ip_address()
        cherrypy.session['logged_in'] = False
        cherrypy.session['username'] = None
        login_template = mako.template.Template(
            filename='templates/login_form.html')
        html = login_template.render(address=address)
        return html

    @cherrypy.expose
    def index(self, username=None, password=None):
        template_dir = os.getcwd() + '/templates/'
        mako.lookup.TemplateLookup(directories=[template_dir])
        address = get_ip_address()
        if 'logged_in' in cherrypy.session:
            print(cherrypy.session['logged_in'])
            if cherrypy.session['logged_in'] is True:
                login_template = mako.template.Template(
                    filename='templates/login_success_template.html')
                html = login_template.render(
                    username=cherrypy.session['username'],
                    x=100,
                    address=address)
            else:
                if check_login(username=username, password=password):
                    cherrypy.session['logged_in'] = True
                    cherrypy.session['username'] = username
                    login_template = mako.template.Template(
                        filename='templates/login_success_template.html')
                    html = login_template.render(username=username, x=100,
                                                 address=address)
                else:
                    print("14")
                    cherrypy.session['logged_in'] = False
                    cherrypy.session['username'] = None
                    login_template = mako.template.Template(
                        filename='templates/login_form.html')
                    html = login_template.render(address=address)

        elif username is None or password is None:
            cherrypy.session['logged_in'] = False
            cherrypy.session['username'] = None
            login_template = mako.template.Template(
                filename='templates/login_form.html')
            html = login_template.render(address=address)
        else:
            if check_login(username=username, password=password):
                cherrypy.session['logged_in'] = True
                cherrypy.session['username'] = username
                login_template = mako.template.Template(
                    filename='templates/login_success_template.html')
                html = login_template.render(username=username, x=100,
                                             address=address)
            else:
                cherrypy.session['logged_in'] = False
                cherrypy.session['username'] = None
                login_template = mako.template.Template(
                    filename='templates/login_form.html')
                html = login_template.render(address=address)

        return html

if __name__ == '__main__':

    print("Creating and Starting DB Thread")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    print("Creating Twitter Thread")
    twitter_queue = queue.Queue()
    twitter_task = twitter.TwitterThread(config_file=config_file,
                                         response_queue=response_queue,
                                         db_queue=db_queue)
    twitter_thread = threading.Thread(target=twitter_task.run, daemon=True)
    twitter_thread.start()

    print("Creating Database")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "webserver_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    print("Create SMS Table")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "sms_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    print("Create Twitter Table")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "twitter_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    cherrypy.config.update({'tools.sessions.on': True,
                            'tools.sessions.timeout': 10
                        })
    cherrypy.config.update({'server.socket_port': 5000})
    try:
        cherrypy.quickstart(Root(), '/')
    except:
        db.kill()

