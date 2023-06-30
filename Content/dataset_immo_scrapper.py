from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd
import concurrent
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor, as_completed
import time
import csv

class Immo_Scrapper:
    
    def __init__(self):
        self.data_immo = []

    def get_links(self, pagesToSearch=1):
        """
        Function that gets links of all houses
        """
        s = requests.Session()
        listOfLinks = []
        listOfLinksFinal = []
        #pagesToSearch = 1 # set the number according to how many pages you want to sarch thru each of properties set
        propertiesToSearch = ["apartment","house"] # fill the list with propertis to search

        for prop in propertiesToSearch:
            for x in range(1,pagesToSearch+1):
                search_url = f"https://www.immoweb.be/en/search/{prop}/for-sale?countries=BE&isNewlyBuilt=false&isAPublicSale=false&page={x}&orderBy=relevance"
                r = s.get(search_url)
                soup = BeautifulSoup(r.text,"html.parser")
                for elem in soup.find_all("a", attrs = {"class": "card__title-link"}):
                    listOfLinks.append(elem.get('href'))
                listOfLinks = listOfLinks[0:len(listOfLinks)-30]
                listOfLinksFinal = listOfLinksFinal + listOfLinks
                listOfLinks.clear()
        return(listOfLinksFinal)

    """with open('links.txt','w+') as file:
        file.write('\n'.join(links))"""

    def get_data(self, url):
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


    
    def save(self, new_data):
            '''This function saves the information acquired from the previous functions and store them in a csv file in the disk.'''
            self.data_immo.append(new_data)
            dataframe_immo = pd.DataFrame(self.data_immo)
            dataframe_immo.to_csv("./dataset-immo.csv", index=False, encoding="utf-8")
            print(dataframe_immo)
            return dataframe_immo

