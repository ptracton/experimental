#! /usr/bin/env python3

#
# Taken from https://www.twilio.com/blog/2016/08/getting-started-python-bottle-twilio-sms-mms.html
#

from bottle import (post, request, response, route, run, )
from twilio import twiml
from twilio.rest import TwilioRestClient
import configparser

# copy in your Twilio Account SID and Auth Token from Twilio Console
config_file = "/home/ptracton/.ucla.cfg",
config = configparser.RawConfigParser()
config.read(config_file)
account_sid = config.get("TWILIO", "SID")
auth_token = config.get("TWILIO", "TOKEN")
client = TwilioRestClient(account_sid, auth_token)


@route('/')
def check_app():
    # returns a simple string stating the app is working
    return "Bottle web app up and running!"


@route('/send-sms/<to_number>/<from_number>/<message_body>/')
def outbound_sms(to_number, from_number, message_body):
    # use the Twilio helper library to send an outbound SMS
    # via the REST API
    client.messages.create(to=to_number, from_=from_number,
                           body=message_body)
    # this response is sent back to the web browser client
    return "SMS sent to " + to_number


@post('/twilio')
def inbound_sms():
    twiml_response = twiml.Response()
    # obtain message body from the request. could also get the "To" and
    # "From" phone numbers as well from parameters with those names
    inbound_message = request.forms.get("Body")
    response_message = "I don't understand what you meant...need more code!"
    # we can use the incoming message text in a condition statement
    if inbound_message == "Hello":
        response_message = "Well, hello right back at ya!"
    twiml_response.message(response_message)
    # we return back the mimetype because Twilio needs an XML response
    response.content_type = "application/xml"
    return str(twiml_response)


if __name__ == '__main__':
    # use the Bottle framework run function to start the development server
    run(host='127.0.0.1', port=5000, debug=True, reloader=True)
