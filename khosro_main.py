import requests
from bs4 import BeautifulSoup
import json
import re

url="https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"

req= requests.get(url)
# print(req.status_code)
soup= BeautifulSoup(req.text, "html.parser")
data = soup.find('div',attrs={"class":"container-main-content"}).script.text
#.result = soup.find("script", string=lambda t: "window.dataLayer" in t).string # Script element
Raw_data_InList= re.findall(r"window.classified = (\{.*\})", data)
Raw_data_InDict = json.loads(Raw_data_InList[0]) # Data dictionary
# print(Raw_data_InDict)

def price():
    try:
       property_dict=(Raw_data_InDict["price"])
       print("Price = ",Raw_data_InDict["price"]['mainValue'])
    except:
       print("Price = None")
price()

def living_area():
    try:
       print("Living area = ",property_dict['netHabitableSurface'],"m²")
    except:
      print("Living area = NA")
living_area()

def number_of_rooms():
    try:
       property_dict=(Raw_data_InDict["property"])
       print("Number of rooms = ",property_dict['bedroomCount'])
    except:
       print("Number of rooms = NA")
number_of_rooms()

id_dict = Raw_data_InDict["customers"][0]['location']

def locality():
   try:
       print("City = ",id_dict['locality'])
   except:
       print("City = NA")
   try:
        print("postalCode = ", id_dict['postalCode'])
   except:
        print("postalCode = NA")
   try:
        a=re.findall("\D.*", id_dict['street'])
        print("street = ",  a[0])
   except:
        print("street = NA")
   try:
        if id_dict['number']==None:
         b=re.findall("\d.*", id_dict['street'])
         print("number = ",b[0])
        else:
         print("number = ", id_dict['number'])
   except:
        print("number = NA")
locality()

property_dict=(Raw_data_InDict["property"])
def kitchen():
    try:
       for i in property_dict["kitchen"].keys():
         if i == 'type':
           print("kitchen = ",property_dict["kitchen"]["type"])
    except:
      print("kitchen = NA")
kitchen()

def furnished():
   try:
       for i in Raw_data_InDict["transaction"]["sale"].keys():
             if i =='isFurnished':
               print("Furnished = ",Raw_data_InDict["transaction"]["sale"]["isFurnished"])
   except:
       print("Furnished = NA")
furnished()





