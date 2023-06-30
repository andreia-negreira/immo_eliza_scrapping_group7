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
        property_dict[url]["Price"] = Raw_data_InDict["price"]["mainValue"]
    except KeyError:
        property_dict[url]["Price"] = None
        
    try:
        property_dict[url]["Type of Transaction"] = Raw_data_InDict["transaction"]["type"]
    except KeyError:
        property_dict[url]["Type of Transaction"] = None
    
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
    
    try:
        if bool(Raw_data_InDict["fireplaceExists"]):
            property_dict[url]["Fireplace"] = "Yes"
    except KeyError:
        property_dict[url]["Fireplace"] = "No"
    
    try:
        if bool(Raw_data_InDict["property"]["hasTerrace"]):
            property_dict[url]["Terrace"] = "Yes"
            property_dict[url]["Area Terrace"] = Raw_data_InDict["property"]["terraceSurface"]
    except KeyError:
        property_dict[url]["Terrace"] = "No"
    
    try:
        if bool(Raw_data_InDict["property"]["hasGarden"]):
            property_dict[url]["Garden"] = "Yes"
            property_dict[url]["Area Garden"] = Raw_data_InDict["property"]["gardenSurface"]
    except KeyError:
        property_dict[url]["Garden"] = "No"
    
    try:
        property_dict[url]["Land Surface"] = Raw_data_InDict["property"]["land"]["surface"]
    except KeyError:
        property_dict[url]["Land Surface"] = None
    
    # surface area of the plot of land
    
    try:
        property_dict[url]["Nº facades"] = Raw_data_InDict["property"]["building"]["facadeCount"]
    except KeyError:
        property_dict[url]["Nº facades"] = None
    
    try:
        if bool(Raw_data_InDict["fhasSwimmingPool"]):
            property_dict[url]["Swimming Pool"] = "Yes"
    except KeyError:
        property_dict[url]["Swimming Pool"] = "No"
        
    try:
        property_dict[url]["State Building"] = Raw_data_InDict["property"]["building"]["condition"]
    except KeyError:
        property_dict[url]["State Building"] = None
            
    return property_dict
    
get_data()

data_immo = {}
def save(new_data):
        '''This function saves the information acquired from the previous functions and store them in a csv file in the disk.'''
        global data_immo
        data_immo.update(new_data)
        dataframe_immo = pd.DataFrame(data_immo)
        dataframe_immo.to_csv("./dataset-immo.csv", sep=" ", index=False)
        return dataframe_immo
    
save()
    
'''

def test():
    url_test = "https://www.immoweb.be/en/search-results/house/for-sale?customerIds=3151988&page=1&orderBy=newest"
    req_test = requests.get(url_test).json()
    print(req_test)

r = test()
py_dict = json.load(r)
print(py_dict)
'''


    