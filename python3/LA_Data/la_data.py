#! /usr/bin/env python3

import os

import googlemaps
import sodapy

if __name__ == "__main__":
    lacity_data_user_id = os.environ['LACITY_DATA_USER_ID']
    lacity_data_token = os.environ['LACITY_DATA_TOKEN']
    lacity_data_password = os.environ['LACITY_DATA_PASSWORD']

    google_token = os.environ['GOOGLE_TOKEN']
    google_user_id = os.environ['GOOGLE_USER_ID']

    #URL = 'data.lacity.org'
    # Library Performance Metrics
    #DATA_ID = 'kkby-9hji'
    # LAPD-Crime-and-Collision-Raw-Data-for-2015
    #DATA_ID = 'ttiz-7an8'
    
    #URL = 'controllerdata.lacity.org'
    #DATA_ID = 'anqa-iu8a'
    
    URL = 'sandbox.demo.socrata.com'    
    DATA_ID = 'nimj-3ivp'
    
    client = sodapy.Socrata(URL, lacity_data_token, username=lacity_data_user_id, password=lacity_data_password)
    data = client.get(DATA_ID, content_type="json", limit=20)
    client.get_metadata(DATA_ID, content_type="json")
    #client.download_attachments(DATA_ID)
    client.close()
    print (data)
    
    gmaps = googlemaps.Client(key=google_token)
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    print (geocode_result)
