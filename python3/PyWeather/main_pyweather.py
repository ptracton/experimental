#! /usr/bin/env python3

'''
Created on Apr 27, 2013

@author: ptracton
'''

import sys
import configparser
from pprint import *
from PyQt4.QtGui import *
import PyWeather
import PyWeatherGUI

if __name__ == '__main__':

#    weather = PyWeather.PyWeather("6f7abstfwn3jst5guawgje4g", "93063")
#    request = weather.GetRequest()
#    pprint(request[0]['query'])
#    pprint(request[0]['type'])
#    current = weather.GetCurrentConditions()
#    pprint (current)
#    print (str(current[0]['temp_F']))       




    app = QApplication(sys.argv)
    gui = PyWeatherGUI.PyWeatherGUI()
    gui.show()
    app.exec_()    
    
    pass
