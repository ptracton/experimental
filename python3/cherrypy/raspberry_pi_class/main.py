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


class Root(object):
    """
    Our cherrypy webserver
    """
    @cherrypy.expose
    def index(self):
        template_dir = os.getcwd() + '/templates/'
        mako.lookup.TemplateLookup(directories=[template_dir])
        login_template = mako.template.Template(
            filename='templates/login_form.html')
        return login_template.render(address=get_ip_address())

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
    
    cherrypy.quickstart(Root(), '/')
