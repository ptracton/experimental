#! /usr/bin/env python3

import os
#https://pypi.python.org/pypi/omdb/0.9.1
import omdb
import requests

if __name__ == "__main__":
    print("OMDB Example Code")
    omdb_api_key = os.environ['OMDB_API_KEY']
    print(omdb_api_key)
    client = omdb.OMDBClient(apikey=omdb_api_key)
    avatar = client.get(title='Avatar')
    print(avatar)
    avatar_post_url = avatar['poster']
    r = requests.get(avatar_post_url)
    #https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
    open('avatar_poster.jpg', 'wb').write(r.content)
    
    
