import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import re
import pandas as pd
import csv
import time
import concurrent

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

async def get_data(url):
    #url="https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"
    s = requests.Session()
    req= s.get(url)

    soup= BeautifulSoup(req.text, "html.parser")
    data = soup.find('div',attrs={"class":"container-main-content"}).script.text

    Raw_data_InList= re.findall(r"window.classified = (\{.*\})", data)
    Raw_data_InDict = json.loads(Raw_data_InList[0]) # Data dictionary


    property_dict = {"url":url}
    
    try:
        property_dict["Locality"] = Raw_data_InDict["customers"][0]['location']['locality']
    except KeyError:
        property_dict["Locality"] = None
    except TypeError:
        property_dict["Locality"] = None
        
    try:
        property_dict["Type of property"] = Raw_data_InDict["property"]["type"]
    except KeyError:
        property_dict["Type of property"] = None
    except TypeError:
        property_dict["Type of property"] = None
    try:
        property_dict["Subtype of property"] = Raw_data_InDict["property"]["subtype"]
    except KeyError:
        property_dict["Subtype of property"] = None
    except TypeError:
        property_dict["Subtype of property"] = None

    try:
        property_dict["Price"] = Raw_data_InDict["price"]["mainValue"]
    except KeyError:
        property_dict["Price"] = None
    except TypeError:
        property_dict["Price"] = None
    
    try:
        property_dict["Type of Transaction"] = Raw_data_InDict["transaction"]["type"]
    except KeyError:
        property_dict["Type of Transaction"] = None
    except TypeError:
        property_dict["Type of Transaction"] = None
    
    try:
        property_dict["Nº rooms"] = Raw_data_InDict["property"]["bedroomCount"]
    except KeyError:
        property_dict["Nº rooms"] = None
    except TypeError:    
        property_dict["Nº rooms"] = None

    try:
        property_dict["Living area"] = Raw_data_InDict["netHabitableSurface"]
    except KeyError:
        property_dict["Living area"] = None
    except TypeError:
        property_dict["Living area"] = None

    try:
        if bool(Raw_data_InDict["property"]["kitchen"]['type']):
            property_dict["Equipped kitchen"] = "Yes"
    except KeyError:
        property_dict["Equipped kitchen"] = "No"
    except TypeError: #added this except for NoneType' object is not subscriptable
        property_dict["Equipped kitchen"] = "No"

    try:
        if bool(Raw_data_InDict["property"]["transaction"]["sale"]["isFurnished"]):
            property_dict["Furnished"] = "Yes"
    except KeyError:
        property_dict["Furnished"] = "No"
    except TypeError:
        property_dict["Furnished"] = "No"

    try:
        if bool(Raw_data_InDict["fireplaceExists"]):
            property_dict["Fireplace"] = "Yes"
    except KeyError:
        property_dict["Fireplace"] = "No"
    except TypeError:
        property_dict["Fireplace"] = "No"
    
    try:
        if bool(Raw_data_InDict["property"]["hasTerrace"]):
            property_dict["Terrace"] = "Yes"
            property_dict["Area Terrace"] = Raw_data_InDict["property"]["terraceSurface"]
    except KeyError:
        property_dict["Terrace"] = "No"
    except TypeError:
        property_dict["Terrace"] = "No"

    try:
        if bool(Raw_data_InDict["property"]["hasGarden"]):
            property_dict["Garden"] = "Yes"
            property_dict["Area Garden"] = Raw_data_InDict["property"]["gardenSurface"]
    except KeyError:
        property_dict["Garden"] = "No"
    except TypeError:
        property_dict["Garden"] = "No"

    try:
        property_dict["Land Surface"] = Raw_data_InDict["property"]["land"]["surface"]
    except KeyError:
        property_dict["Land Surface"] = None
    except TypeError: #added this except for NoneType' object is not subscriptable
        property_dict["Land Surface"] = None
    
    # surface area of the plot of land
    
    try:
        property_dict["Nº facades"] = Raw_data_InDict["property"]["building"]["facadeCount"]
    except KeyError:
        property_dict["Nº facades"] = None
    except TypeError:
        property_dict["Nº facades"] = None
    
    try:
        if bool(Raw_data_InDict["fhasSwimmingPool"]):
            property_dict["Swimming Pool"] = "Yes"
    except KeyError:
        property_dict["Swimming Pool"] = "No"
    except TypeError:
        property_dict["Swimming Pool"] = "No"
        
    try:
        property_dict["State Building"] = Raw_data_InDict["property"]["building"]["condition"]
    except KeyError:
        property_dict["State Building"] = None
    except TypeError:
        property_dict["State Building"] = None
            
    return property_dict



def save(new_data):
        data_immo = []
        '''This function saves the information acquired from the previous functions and store them in a csv file in the disk.'''
        data_immo.append(new_data)
        dataframe_immo = pd.DataFrame(data_immo)
        dataframe_immo.to_csv("./dataset-immo.csv", index=False, encoding="utf-8")
        print(dataframe_immo)
        return dataframe_immo

start = time.time()
links = get_links(167)
end = time.time()
print("Gathering links time: {:.6f}s".format(end-start))

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_data, link) for link in links]
    for future in concurrent.futures.as_completed(futures):
        save(future.result())        
end = time.time()
print("Time taken for gathering data from {} links: {:.6f}s".format(len(links),end-start))

save()
    
'''  
with open("./dataset-immo.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=new_data.keys())
            writer.writeheader()
            writer.writerow(new_data)  
            return writer
data_immo = {}
global data_immo
        data_immo.update(new_data)
        dataframe_immo = pd.DataFrame(data_immo)
        dataframe_immo.to_csv("./dataset-immo.csv", sep=" ", index=False)
        return dataframe_immo
        
def test():
    url_test = "https://www.immoweb.be/en/search-results/house/for-sale?customerIds=3151988&page=1&orderBy=newest"
    req_test = requests.get(url_test).json()
    print(req_test)

r = test()
py_dict = json.load(r)
print(py_dict)
'''


    