#!/usr/bin/env python3
'''
Following along and implementing code from https://www.youtube.com/watch?v=3xQTJi2tqgk

'''

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    REQ = requests.get(
        "http://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=Northridge%2C+CA")

    # print(REQ.content)
    soup = BeautifulSoup(REQ.content)
    # print(soup.prettify().encode('ascii', 'ignore'))
    # print(soup.get_text().encode('utf-8', 'replace'))

    # List of all links!
    links = soup.find_all("a")
    paragraphs = []
    for x in links:
        y = str(x).encode('ascii', 'ignore').decode('ascii')
        # print(y)
        paragraphs.append(y)
        del y
        # if "http" in (x.get("href")).encode('ascii', 'ignore').decode('ascii'):
        url_string = "<a href = \"%s\">%s</a>" % (
            x.get("href"), (x.text).encode('ascii', 'ignore').decode('ascii'))
        # print(url_string)
    # print(paragraphs)

    g_data = soup.find_all("div", {"class": "info"})
    # print(g_data)
    for ITEM in g_data:
        print("\n")
        try:
            print(ITEM.contents[0].find_all("a", {"class": "business-name"})[0].text)
            #print(ITEM.contents[1].find_all("p", {"class": "adr"})[0].text)
            print(ITEM.contents[1].find_all("span", {"itemprop": "streetAddress"})[0].text)
            print(ITEM.contents[1].find_all(
                "span", {"itemprop": "addressLocality"})[0].text.replace(',', ''))
            print(ITEM.contents[1].find_all("span", {"itemprop": "addressRegion"})[0].text)
            print(ITEM.contents[1].find_all("span", {"itemprop": "postalCode"})[0].text)
            print(ITEM.contents[1].find_all("li", {"class": "phone"})[0].text)
        except:
            pass
        #print(ITEM.contents[0].text, ITEM.contents[1].text)
