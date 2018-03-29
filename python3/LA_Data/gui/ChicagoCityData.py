import os
import sodapy

chicagocity_app_token = os.environ['LA_CITY_APP_TOKEN']
chicagocity_secret_token = os.environ['LA_CITY_SECRET_TOKEN']
chicagocity_password = os.environ['LA_CITY_PASSWORD']
chicagocity_user_name = "ptracton@hotmail.com"
chicagocity_url = 'data.cityofchicago.org/'


class ChcagoCityData:
    def __init__(self, data_id=None):
        self.data_id = data_id
        self.data = None
        self.client = sodapy.Socrata(
            domain=chicagocity_url,
            app_token=chicagocity_app_token,
            username=chicagocity_user_name,
            password=chicagocity_password)
        return

    def get_data(self):
        self.data = self.client.get(self.data_id)
        return
