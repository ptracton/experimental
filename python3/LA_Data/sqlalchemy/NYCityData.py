import os
import sodapy

nyccity_app_token = os.environ['LA_CITY_APP_TOKEN']
nyccity_secret_token = os.environ['LA_CITY_SECRET_TOKEN']
nyccity_password = os.environ['LA_CITY_PASSWORD']
nyccity_user_name = "ptracton@hotmail.com"
nyccity_url = 'data.cityofnewyork.us/'


class NYCityData:
    def __init__(self, data_id=None):
        self.data_id = data_id
        self.data = None
        self.client = sodapy.Socrata(
            domain=nyccity_url,
            app_token=nyccity_app_token,
            username=nyccity_user_name,
            password=nyccity_password)
        return

    def get_data(self):
        self.data = self.client.get(self.data_id)
        return
