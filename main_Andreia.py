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

def get_data():
    url="https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"
    req= requests.get(url)

    soup= BeautifulSoup(req.text, "html.parser")
    data = soup.find('div',attrs={"class":"container-main-content"}).script.text

    Raw_data_InList= re.findall(r"window.classified = (\{.*\})", data)
    Raw_data_InDict = json.loads(Raw_data_InList[0]) # Data dictionary


    property_dict = {}
    property_dict[url] = {}
    
    try:
        property_dict[url]["Locality"] = Raw_data_InDict["customers"][0]['location']['locality']
    except KeyError:
        property_dict[url]["Locality"] = None
        
    try:
        property_dict[url]["Type of property"] = Raw_data_InDict["property"]["type"]
    except KeyError:
        property_dict[url]["Type of property"] = None
    
    try:
        property_dict[url]["Subtype of property"] = Raw_data_InDict["property"]["subtype"]
    except KeyError:
        property_dict[url]["Subtype of property"] = None
    
    try:
        property_dict[url]["price"] = Raw_data_InDict["price"]["mainValue"]
    except KeyError:
        property_dict[url]["price"] = None
    
    # type of sale (exclusion of life sales)
    
    try:
        property_dict[url]["Nº rooms"] = Raw_data_InDict["property"]["bedroomCount"]
    except KeyError:
        property_dict[url]["Nº rooms"] = None    

    try:
        property_dict[url]["Living area"] = Raw_data_InDict["netHabitableSurface"]
    except KeyError:
        property_dict[url]["Living area"] = None

    try:
        if bool(Raw_data_InDict["property"]["kitchen"]['type']):
            property_dict[url]["Equipped kitchen"] = "Yes"
    except KeyError:
        property_dict[url]["Equipped kitchen"] = "No"
        
    try:
        if bool(Raw_data_InDict["transaction"]["sale"]["isFurnished"]):
            property_dict[url]["Furnished"] = "Yes"
    except KeyError:
        property_dict[url]["Furnished"] = "No"
        
    try:
        property_dict[url]["Furnished"] = Raw_data_InDict["transaction"]["sale"]["isFurnished"]
    except KeyError:
        property_dict[url]["Furnished"] = None
    
    # open fire (yes/no)
    
    # terrace (yes/no) --> if yes: area
    
    # garden (yes/no) --> if yes: area
    
    # surface of the land
    
    # surface area of the plot of land
    
    # number of facades
    
    # swimming pool
    
    # state of the building (new, to be renovated, etc.)
            
    return property_dict
    
get_data()

def save():
        '''This function saves the information acquired from the previous functions and store them in a csv file in the disk.'''
        data_immo = get_data()
        dataframe_immo = pd.DataFrame(data_immo)
        dataset_csv = dataframe_immo.to_csv("./dataset-immo.csv", sep=" ", index=False)
        return dataset_csv
    

save({'Name': ['Tom', 'Jack', 'nick', 'juli'],
        'marks': [99, 98, 95, 90]})
    
'''

def test():
    url_test = "https://www.immoweb.be/en/search-results/house/for-sale?customerIds=3151988&page=1&orderBy=newest"
    req_test = requests.get(url_test).json()
    print(req_test)

r = test()
py_dict = json.load(r)
print(py_dict)
'''


    