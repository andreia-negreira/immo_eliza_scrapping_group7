from bs4 import BeautifulSoup
import requests
import json
import re

def get_links(pagesToSearch=1):
    """
    Function that gets links of all houses
    """
    s = requests.Session()
    listOfLinks = []
    listOfLinksFinal = []
    #pagesToSearch = 1 # set the number according to how many pages you want to sarch thru each of properties set
    propertiesToSearch = ["house","apartment"] # fill the list with propertis to search

    for prop in propertiesToSearch:
        for x in range(1,pagesToSearch+1): #houses
            search_url = f"https://www.immoweb.be/en/search/{prop}/for-sale?countries=BE&priceType=SALE_PRICE&page={x}&orderBy=relevance"
            r = s.get(search_url)
            soup = BeautifulSoup(r.text,"html.parser")
            for elem in soup.find_all("a", attrs = {"class": "card__title-link"}):
                listOfLinks.append(elem.get('href'))
            listOfLinks = listOfLinks[0:len(listOfLinks)-30]
            listOfLinksFinal = listOfLinksFinal + listOfLinks
            listOfLinks.clear()
    return(listOfLinksFinal)

links = get_links(2)

with open('links.txt','w+') as file:
    file.write('\n'.join(links))