import os
import sodapy

lacity_app_token = os.environ['LA_CITY_APP_TOKEN']
lacity_secret_token = os.environ['LA_CITY_SECRET_TOKEN']
lacity_password = os.environ['LA_CITY_PASSWORD']
lacity_user_name = "ptracton@hotmail.com"
lacity_url = 'data.lacity.org'


class LACityData:
    def __init__(self, data_id=None):
        self.data_id = data_id
        self.data = None
        self.client = sodapy.Socrata(
            domain=lacity_url,
            app_token=lacity_app_token,
            username=lacity_user_name,
            password=lacity_password)
        return

    def get_data(self):
        self.data = self.client.get(self.data_id)
        return
