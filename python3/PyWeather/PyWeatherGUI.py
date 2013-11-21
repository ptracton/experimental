
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import configparser
import PyWeather

class PyWeatherGUI(QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(PyWeatherGUI, self).__init__(parent)

        try:
            config = configparser.SafeConfigParser()
            config.read( "temperature_config.ini" )
        except:
            print("Config fail")            
            sys.exit()

        self.location = config['Temperature']['location']
        self.key = config['Temperature']['key']
        self.temperature_display = config['Temperature']['temperature_display']
        self.wind_speed_display = config['Temperature']['wind_speed']
        
        self.weather = PyWeather.PyWeather(self.key, self.location)
        current_weather = self.weather.GetCurrentConditions()
        
        top_layout = QVBoxLayout()

        #######################################################################
        #
        # Request Display
        #
        #######################################################################        
        request_layout = QHBoxLayout()
        request_left_layout = QVBoxLayout()
        request_right_layout = QVBoxLayout()
        request = self.weather.GetRequest()
        self.RequestLabel = QLabel("%s:" % request[0]['type'])
        self.RequestValue = QLabel("%s" % request[0]['query']) 

        request_left_layout.addWidget(self.RequestLabel)
        request_right_layout.addWidget(self.RequestValue)
        request_layout.addLayout(request_left_layout)
        request_layout.addLayout(request_right_layout)

        #######################################################################
        #
        # Temperature Display
        #
        #######################################################################        
        temperature_layout = QHBoxLayout()
        temperature_left_layout = QVBoxLayout()
        temperature_right_layout = QVBoxLayout()

        self.TemperatureLabel = QLabel("Current Temperature:")
        self.TemperatureValue = QLabel("%s" % current_weather[0][self.temperature_display])

        temperature_left_layout.addWidget(self.TemperatureLabel)
        temperature_right_layout.addWidget(self.TemperatureValue)
        temperature_layout.addLayout(temperature_left_layout)
        temperature_layout.addLayout(temperature_right_layout)

        #######################################################################
        #
        # Humidity Display
        #
        #######################################################################        
        humidity_layout = QHBoxLayout()
        humidity_left_layout = QVBoxLayout()
        humidity_right_layout = QVBoxLayout()

        self.HumidityLabel = QLabel("Current Humidity:")
        self.HumidityValue = QLabel("%s " % current_weather[0]['humidity'])

        humidity_left_layout.addWidget(self.HumidityLabel)
        humidity_right_layout.addWidget(self.HumidityValue)
        humidity_layout.addLayout(humidity_left_layout)
        humidity_layout.addLayout(humidity_right_layout)

        #######################################################################
        #
        # Precipitation Display
        #
        #######################################################################        
        precipitation_layout = QHBoxLayout()
        precipitation_left_layout = QVBoxLayout()
        precipitation_right_layout = QVBoxLayout()

        self.PrecipitationLabel = QLabel("Current Precipitation:")
        self.PrecipitationValue = QLabel("%s " % current_weather[0]['precipMM'])

        precipitation_left_layout.addWidget(self.PrecipitationLabel)
        precipitation_right_layout.addWidget(self.PrecipitationValue)
        precipitation_layout.addLayout(precipitation_left_layout)
        precipitation_layout.addLayout(precipitation_right_layout)

        #######################################################################
        #
        # Description Display
        #
        #######################################################################        
        description_layout = QHBoxLayout()
        description_left_layout = QVBoxLayout()
        description_right_layout = QVBoxLayout()

        self.DescriptionLabel = QLabel("Current Description:")
        self.DescriptionValue = QLabel("%s " % current_weather[0]['weatherDesc'][0]['value'])

        description_left_layout.addWidget(self.DescriptionLabel)
        description_right_layout.addWidget(self.DescriptionValue)
        description_layout.addLayout(description_left_layout)
        description_layout.addLayout(description_right_layout)        

        #######################################################################
        #
        # Wind_Direction Display
        #
        #######################################################################        
        wind_direction_layout = QHBoxLayout()
        wind_direction_left_layout = QVBoxLayout()
        wind_direction_right_layout = QVBoxLayout()

        self.Wind_DirectionLabel = QLabel("Current Wind_direction:")
        self.Wind_DirectionValue = QLabel("%s " % current_weather[0]['winddir16Point'])

        wind_direction_left_layout.addWidget(self.Wind_DirectionLabel)
        wind_direction_right_layout.addWidget(self.Wind_DirectionValue)
        wind_direction_layout.addLayout(wind_direction_left_layout)
        wind_direction_layout.addLayout(wind_direction_right_layout)

        #######################################################################
        #
        # Wind_speed Display
        #
        #######################################################################        
        wind_speed_layout = QHBoxLayout()
        wind_speed_left_layout = QVBoxLayout()
        wind_speed_right_layout = QVBoxLayout()

        self.Wind_SpeedLabel = QLabel("Current Wind_speed:")
        self.Wind_SpeedValue = QLabel("%s " % current_weather[0][self.wind_speed_display])

        wind_speed_left_layout.addWidget(self.Wind_SpeedLabel)
        wind_speed_right_layout.addWidget(self.Wind_SpeedValue)
        wind_speed_layout.addLayout(wind_speed_left_layout)
        wind_speed_layout.addLayout(wind_speed_right_layout)         
        
        #######################################################################
        #
        # Top Level Display
        #
        #######################################################################
        top_layout.addLayout(request_layout)
        top_layout.addLayout(temperature_layout)
        top_layout.addLayout(humidity_layout)
        top_layout.addLayout(precipitation_layout)
        top_layout.addLayout(description_layout)
        top_layout.addLayout(wind_direction_layout)
        top_layout.addLayout(wind_speed_layout)
        
        self.setLayout(top_layout)        
        self.setWindowTitle("Python Weather GUI")

        return
