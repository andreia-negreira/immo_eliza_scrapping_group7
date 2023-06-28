from bs4 import BeautifulSoup
import requests
import json
import re

def get_links():
    """
    Function that gets links of all houses
    """
    s = requests.Session()
    listOfLinks = []
    listOfLinksFinal = []
    pagesToSearch = 10 # set the number according to how many pages you want to sarch thru
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

links = get_links()


"""
def get_data():
    url ="https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.find('div',attrs = {"class":"container-main-content"}).script.text
    test = re.findall(r"window.classified = ({.*})", data)
    result = json.loads(test[0]) # Data dictionary 
    return result
"""