#! /usr/bin/env python3

"""
DEFAULT LIBRARIES
"""
import configparser
import datetime
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
import SystemState
import twitter

"""
GLOBALS
"""
db_queue = queue.Queue()
db = database.Database(database_queue=db_queue,
                       database_file_name="webserver_thread.db")

response_queue = queue.Queue()

# copy in your Twilio Account SID and Auth Token from Twilio Console
config_file = "/home/pi/.ucla.cfg",
config = configparser.RawConfigParser()
config.read(config_file)
command_list = config.get("COMMANDS", "TERMS")
account_sid = config.get("TWILIO", "SID")
auth_token = config.get("TWILIO", "TOKEN")
TwilioClient = twilio.rest.TwilioRestClient(account_sid, auth_token)

SystemStateQueue = queue.Queue()
SystemStateInst = SystemState.SystemStateThread(
    SystemStateQueue=SystemStateQueue, db_queue=db_queue)


def get_ip_address():
    """
    Get the server IP address without using the /etc/hosts file
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip


def get_SystemState():
    """
    Get the current System State
    """
    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_GetState,
        response_queue=response_queue)

    SystemStateQueue.put(message)

    while response_queue.empty():
        pass

    response = response_queue.get()
    return response


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

    def store_sms_message(self, message_from=None, message_body=None):
        if message_from is None or message_body is None:
            return
        now = datetime.datetime.now()
        db_data = {}
        db_data[0] = ('SMS_FROM', """ "{}" """.format(message_from))
        db_data[1] = ('SMS_TEXT', """ "{}" """.format(message_body))
        db_data[2] = ('SMS_DATE', """ "{}" """.format(
            now.strftime("%m-%d-%Y")))
        db_data[3] = ('SMS_TIME', """time("{}")""".format(
            now.strftime("%H:%M:%S")))
        print("StoreSMSMessage {}".format(db_data))
        data_message = database.DatabaseDataMessage(
            table_name="sms", data_dict=db_data
        )
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_DATA,
            message=data_message)
        db_queue.put(message)

        return
    
    def process_sms_message(self, message_body=None):
        """
        """
        print("ProcessSMSMessage {} {}".format(message_body,
                                               len(message_body)))
        if message_body is None:
            return
        message_body_list = message_body.split(" ")
        message_body_upper = message_body_list[0].upper()
        data = ""
        print("BODY LIST {}".format(message_body_list))
        print("BODY UPPER {}".format(message_body_upper))

        if message_body_upper == "RASPI-LED":
            command = SystemState.SystemStateCommand.SYSTEM_STATE_LED
            print("SMSL_COMMAND = {}".format(command))

        elif message_body_upper == "RASPI-LCD":
            command = SystemState.SystemStateCommand.SYSTEM_STATE_Picture
            data = message_body_list[1:]
            print("SMSD_COMMAND = {}".format(command))
            
        elif message_body_upper == "RASPI-PICTURE":
            command = SystemState.SystemStateCommand.SYSTEM_STATE_Picture
            print("SMSP_COMMAND = {}".format(command))

        message = SystemState.SystemStateMessage(command=command, data=data)
        SystemStateQueue.put(message)
        return
    
    @cherrypy.expose
    def twilio(self, **params):
        """
        TODO: check if the 'From' is a valid phone we want to act on
        """
        
        print("\n\nTWILIO: {}".format(params.keys()))
        if 'From' in params.keys():
            message_from = params['From']
        else:
            message_from = "Unknown"

        if 'Body' in params.keys():
            message_body = params['Body']
        else:
            message_body = "Unknown"

        self.store_sms_message(message_from, message_body)
        self.process_sms_message(message_body)
#        if 'Body' in params.keys():
#            body = params['Body']
#            print(body)
        response_message = "ACK!"
        twiml_response = twiml.Response()
        twiml_response.message(response_message)
        return str(twiml_response)

    @cherrypy.expose
    def MotionSensorEnabledButton(self, MotionSensorEnabledButton=None):
        raise cherrypy.HTTPRedirect("/")
        return

    @cherrypy.expose
    def LEDButton(self, LEDButton=None):
        print("LED Button Pressed! {}".format(LEDButton))
        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_LED,
            response_queue=None)

        SystemStateQueue.put(message)
        raise cherrypy.HTTPRedirect("/")
        return

    @cherrypy.expose
    def LCDButton(self, LCDButton=None, LCDString=None):
        print("LCDButton {}".format(LCDString))
        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_LCD,
            data=LCDString,
            response_queue=None)
        SystemStateQueue.put(message)
        raise cherrypy.HTTPRedirect("/")
        return

    @cherrypy.expose
    def SystemEnabledButton(self, SystemEnabledButton=None):
        print("System Enabled Button Pressed! {}".format(SystemEnabledButton))
        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_SystemEnabled,
            response_queue=None)

        SystemStateQueue.put(message)
        raise cherrypy.HTTPRedirect("/")
        return

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
        system_state = get_SystemState()
        if 'logged_in' in cherrypy.session:
            print(cherrypy.session['logged_in'])
            if cherrypy.session['logged_in'] is True:
                login_template = mako.template.Template(
                    filename='templates/login_success_template.html')
                html = login_template.render(
                    username=cherrypy.session['username'],
                    x=100,
                    address=address,
                    SystemEnabled=system_state.SystemEnabled,
                    LED=system_state.Hardware.LED.state,
                    MotionSensor=system_state.Hardware.MotionSensor.state,
                    LCD=system_state.Hardware.LCD.state)
            else:
                if check_login(username=username, password=password):
                    cherrypy.session['logged_in'] = True
                    cherrypy.session['username'] = username
                    login_template = mako.template.Template(
                        filename='templates/login_success_template.html')
                    html = login_template.render(username=username, x=100,
                                                 address=address,
                                                 SystemEnabled=system_state.SystemEnabled,
                                                 LED=system_state.Hardware.LED.state,
                                                 MotionSensor=system_state.Hardware.MotionSensor.state,
                                                 LCD=system_state.Hardware.LCD.state)
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
                                             address=address,
                                             SystemEnabled=system_state.SystemEnabled,
                                             LED=system_state.Hardware.LED.state,
                                             MotionSensor=system_state.Hardware.MotionSensor.state,
                                             LCD=system_state.Hardware.LCD.state)
            else:
                cherrypy.session['logged_in'] = False
                cherrypy.session['username'] = None
                login_template = mako.template.Template(
                    filename='templates/login_form.html')
                html = login_template.render(address=address)

        return html

if __name__ == '__main__':
    print("Creating images directory")
    try:
        os.mkdir("images")
    except:
        pass
    
    print("Creating and Starting DB Thread")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    print("Creating System State Thread")
    SystemStateThread = threading.Thread(target=SystemStateInst.run,
                                         daemon=True)
    SystemStateThread.start()

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

    print("Create Sensor Table")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "sensors_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    print("Create Button Table")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "buttons_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    print("Create Images Table")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "images_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)

    cherrypy.config.update({'tools.sessions.on': True,
                            'tools.sessions.timeout': 10
                        })
    cherrypy.config.update({'server.socket_port': 5000})
#    cherrypy.config.update({'server.socket_host': get_ip_address()})
    try:
        cherrypy.quickstart(Root(), '/')
    except:
        db.kill()
