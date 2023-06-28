import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import re
import pandas as pd

root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&priceType=SALE_PRICE&page=1&orderBy=relevance"
range_links = range(1, 12)

req = requests.get(root_url)

# Getting the cookies
cookies = req.cookies.get_dict()
#print(cookies)
#print(req.status_code)

    
def get_links():
    """
    Function that gets links of all houses and appartments
    """
    s = requests.Session()
    listOfLinks = []
    listOfLinksFinal = []
    pagesToSearch = 3 # set the number accordint to how many pages you want to sarch thru

    for x in range(1,pagesToSearch+1):
        search_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&priceType=SALE_PRICE&page={x}&orderBy=relevance"
        r = s.get(search_url)
        soup = BeautifulSoup(r.text,"html.parser")
        for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
            listOfLinks.append(elem.get('href'))
        listOfLinks = listOfLinks[0:30]
        listOfLinksFinal = listOfLinksFinal + listOfLinks
        listOfLinks.clear()

    return(listOfLinksFinal)
    
'''
def scrapping_general():
    link_immo = "https://www.immoweb.be/en/classified/house/for-sale/libin/6890/10657263"
    r = requests.get(link_immo)
    
    s = requests.Session()
    soup = BeautifulSoup(r.text, "html.parser")
    
    for elem in soup.find_all("td", attrs={"class": "classified-table__data"}):
        print(elem.get(""))
    
scrapping_general()
    


def test():
    url_test = "https://www.immoweb.be/en/search-results/house/for-sale?customerIds=3151988&page=1&orderBy=newest"
    req_test = requests.get(url_test).json()
    print(req_test)

r = test()
py_dict = json.load(r)
print(py_dict)
'''

def get_data():
    url ="https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.find('div',attrs = {"class":"container-main-content"}).script.text
    test = re.findall(r"window.classified = ({.*})", data)
    result = json.loads(test[0]) # Data dictionary

    return result


def save():
        '''This function saves the information acquired from the previous functions and store them in a csv file in the disk.'''
        data_immo = get_data()
        dataframe_immo = pd.DataFrame(data_immo)
        dataset_csv = dataframe_immo.to_csv("./dataset-immo.csv", sep=" ")
        return dataset_csv
    

save({'Name': ['Tom', 'Jack', 'nick', 'juli'],
        'marks': [99, 98, 95, 90]})

    