#! /usr/bin/env python3
'''
Working out the scraping of data from Google nad Yahoo Finance
'''

from bs4 import BeautifulSoup
import requests


def get_list_of_links(soup=None):
    if soup is None:
        return []
    list_of_links = []
    links = soup.find_all("a")
    for x in links:
        y = str(x).encode('ascii', 'ignore').decode('ascii')
        list_of_links.append(y)
        del y

    return list_of_links

if __name__ == "__main__":
    #REQ = requests.get("https://www.google.com/finance?q=MDT")
    #REQ = requests.get("https://www.google.com/finance?q=MSFT")
    #REQ = requests.get("https://www.google.com/finance?q=AAPL")
    REQ = requests.get("https://www.google.com/finance?q=GOOG")
    SOUP = BeautifulSoup(REQ.content)
    # LINKS = get_list_of_links(SOUP)
    # for LINK in LINKS:
    #    print(LINK)
    TITLEW1 = SOUP.find_all("td", {"class": "p linkbtn"})
    EXECUTIVES = []
    for ITEM in TITLEW1:
        for x in range(len(ITEM.contents)):
            if ITEM.contents[x].string is not None:
                EXECUTIVES.append(ITEM.contents[x].string.strip('\n'))
    # print(EXECUTIVES)

    TITLEW1 = SOUP.find_all("td", {"class": "t"})
    TITLES = []
    for ITEM in TITLEW1:
        for x in range(len(ITEM.contents)):
            if ITEM.contents[x].string is not None:
                TITLES.append(ITEM.contents[x].string.strip('\n'))

    count = 0
    for x in TITLES:
        if 'Age' in x:
            del TITLES[count]
        count = count + 1
    # print(TITLES)

    EXEC_TTILES_DICT = dict(zip(EXECUTIVES, TITLES))
    for k, v in EXEC_TTILES_DICT.items():
        print(k.encode('ascii', 'ignore').decode('ascii'),
              v.encode('ascii', 'ignore').decode('ascii'))
