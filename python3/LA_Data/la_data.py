#! /usr/bin/env python3

import os

import sodapy

if __name__ == "__main__":
    lacity_app_token = os.environ['LA_CITY_APP_TOKEN']
    lacity_secret_token = os.environ['LA_CITY_SECRET_TOKEN']
    lacity_password = os.environ['LA_CITY_PASSWORD']
    lacity_user_name = "ptracton@hotmail.com"

    #print("SECRET {}".format(lacity_secret_token))
    #print("TOKEN {}".format(lacity_app_token))
    #print("PASSWORD {}".format(lacity_password))

    #https://data.lacity.org/A-Livable-and-Sustainable-City/Library-Branches/a4nt-4gca
    URL = 'data.lacity.org'
    DATA_ID = 'a4nt-4gca'
    
    #URL = 'sandbox.demo.socrata.com'
    #DATA_ID = 'e8ey-y5bm'

    client = sodapy.Socrata(
        domain=URL,
        app_token=lacity_app_token,
        username=lacity_user_name,
        password=lacity_password)
    data = client.get(DATA_ID)
    #client.get_metadata(DATA_ID)
    #client.download_attachments(DATA_ID)
    client.close()
    print(data)
