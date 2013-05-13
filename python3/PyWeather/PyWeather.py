'''
Created on Apr 27, 2013

@author: ptracton
'''

import datetime
import json
import urllib.request
from pprint import *

class PyWeather(object):
    '''
    classdocs
    '''


    def __init__(self, key = "", location = ""):
        '''
        Constructor
        '''
        self.key = key
        self.timestamp = datetime.datetime.now()
        self.weather_json = ""
        self.DEBUG = False
        self.location = location

        ##
        ## Get the data
        ##
#        self._GetWeather()

    def _GetWeather(self):
        '''
        This is the function that acutally goes out to the website and fetches the data
        '''
        
        self.timestamp = datetime.datetime.now()
        weatherURL = 'http://api.worldweatheronline.com/free/v1/weather.ashx?key=%s&q=%s&num_of_days=3&format=json' % (self.key, self.location)
    
        try:
            weather_page = urllib.request.urlopen(weatherURL)
            
            ##
            ## http://stackoverflow.com/questions/6862770/python-3-let-json-object-accept-bytes-or-let-urlopen-output-strings
            ##
            str_response = weather_page.readall().decode('utf-8')
            self.weather_json = json.loads(str_response)
                    
        except:
            print("Failed to get page")
            return None

        if (self.DEBUG):
            pprint(self.weather_json)
        return

    def GetCurrentConditions(self):
        self._GetWeather()
        return self.weather_json['data']['current_condition']

    def GetRequest(self):
        self._GetWeather()
        return self.weather_json['data']['request']


    def _GetTimeZone(self):
        return


