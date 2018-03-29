#! /usr/bin/env python3

import os
import requests
import newsapi
import re
import pprint
import json

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

if __name__ == "__main__":
    newsapi_key = os.environ['NEWSAPI_KEY']
    api = newsapi.NewsApiClient(api_key=newsapi_key)
    newapi_url = "https://newsapi.org/v2/"
    sources = "sources?apiKey={}".format(newsapi_key)
    
    #print(api.get_sources())
    #print(api.get_top_headlines(sources='bbc-news'))

    r = requests.get(newapi_url+sources)
    text = r.content.decode('utf-8')
    new_text = remove_non_ascii(text)
    new_json = json.loads(new_text)
    #print(new_json['sources'])        
    json_sources = new_json['sources']
    for x in json_sources:
        print("ID: {}".format(x['id']))
        print("Name: {}".format(x['name']))
        print("Description: {}".format(x['description']))
        print("Country: {}".format(x['country']))
        print("Language: {}".format(x['language']))
        print("Category: {}".format(x['category']))
        print("URL: {}\n\n".format(x['url']))
