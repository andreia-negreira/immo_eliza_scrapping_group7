import requests
import pandas
import json
import regex as re
from bs4 import BeautifulSoup
s = requests.Session()
list_all_dict= []

url_all=[]
pages_url=[]
for i in ["house"]:#, "apartment"

     for j in range(1,300):
        print(j)
        search_url = f"https://www.immoweb.be/en/search/{i}/for-sale?countries=BE&isNewlyBuilt=false&isAPublicSale=false&page={j}&orderBy=relevance"
        pages_url.append(search_url)
        for page_url in pages_url:
           r= requests.get(page_url)
           soup = BeautifulSoup(r.text, "html.parser")
           url_All = []
           for url in soup.find_all("a", attrs={"class": "card__title-link"}):
             url_All.append(url.get('href'))
        url_all= url_all+url_All[0:30]

with open("url_house.txt", 'w') as url_house:
   for i in url_all:
      url_house.write(str(i) + '\n')
url_house.close()
# opening the file in read mode
my_file = open("url_house.txt", "r")

# reading the file
data = my_file.read()

# replacing end splitting the text
# when newline ('\n') is seen.
url_house_list = data.split("\n")
print(url_house_list)
my_file.close()



# print(url_all)

print(len(url_all))
# url_all=["https://www.immoweb.be/en/classified/villa/for-sale/waterloo/1410/10666111","https://www.immoweb.be/en/classified/new-real-estate-project-houses/for-sale/geraardsbergen/9500/10666595","https://www.immoweb.be/en/classified/new-real-estate-project-houses/for-sale/alleur/4432/10360969","https://www.immoweb.be/en/classified/villa/for-sale/wetteren/9230/10639285","https://www.immoweb.be/en/classified/house/for-sale/saint-nicolas/4420/10666853"]

# for i in url_all:

#     req= requests.get(i)
#     # print(req.status_code)
#     soup= BeautifulSoup(req.text, "html.parser")
#     data = soup.find('div',attrs={"class":"container-main-content"}).script.text
#     #.result = soup.find("script", string=lambda t: "window.dataLayer" in t).string # Script element
#     Raw_data_InList= re.findall(r"window.classified = (\{.*\})", data)
#     Raw_data_InDict = json.loads(Raw_data_InList[0]) # Data dictionary
#     # print(Raw_data_InList)


#     def price():
#         try:
#            property_dict=(Raw_data_InDict["price"])
#            return Raw_data_InDict["price"]['mainValue']
#         except:
#            return  "No info"
#     price()


#     def living_area():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#            return property_dict['netHabitableSurface']
#         except:
#           return None
#     living_area()

#     def number_of_rooms():
#         try:
#            property_dict=(Raw_data_InDict["property"])
#            return property_dict['bedroomCount']
#         except:
#            return "Number of rooms = NA"
#     number_of_rooms()


#     id_dict = Raw_data_InDict["customers"][0]['location']

#     def locality():
#        try:
#            return id_dict['locality']
#        except:
#            return "No info"
#        locality()
#     def postcode():  
#        try:
#             return id_dict['postalCode']
#        except:
#             return None
#        postcode()
#     def street():        
#        try:
#             a=re.findall(r'\D*', id_dict['street'])
#             return a[0]
#        except:
#             return "No info"
#     street()
#     def property_number():
#        try:
#             if id_dict['number']==None:
#              b=re.findall(r'\d[\d/]*[A-Za-z]*',id_dict['street'])
#              return b[0]
#             else:
#              return id_dict['number']
#        except:
#             return "No info"
#     property_number()   
    

#     property_dict=(Raw_data_InDict["property"])
#     def kitchen():
#         try:
#            for i in property_dict["kitchen"].keys():
#              if i == 'type' and property_dict["kitchen"]["type"]=='INSTALLED':
#                return "Yes"
#              else:
#                  return "No"
#         except:
#           return "No info"
#     kitchen()


#     def furnished():
#        try:
#           for i in Raw_data_InDict["transaction"]["sale"].keys():
#              # print(i)
#              if i =='isFurnished':
#                if Raw_data_InDict["transaction"]["sale"]["isFurnished"]==None:
#                 return "No"
#                else:
#                 return "Yes"
#        except:
#          return "No info"



#     def terrace():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'hasTerrace' and property_dict[key] == True:
#                    return "Yes"

#                 if key == 'hasTerrace' and property_dict[key] == None:
#                    return "No"
#         except:
#              return "No info"
#     terrace()

#     def terrace_area():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'terraceSurface' :
#                    return property_dict[key]

#                 if key == 'terraceSurface' and property_dict[key] == None:
#                    return None
#         except:
#              return "No info"
#     terrace()


#     def garden():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'hasGarden' and property_dict[key] == True:
#                    return "Yes"

#                 if key == 'hasGarden' and property_dict[key] == None:
#                    return "No"
#         except:
#              return "No info"
#     garden()
#     def garden_area():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'gardenSurface':
#                    return property_dict[key]

#                 elif key == 'gardenSurface' and (property_dict[key] == False):
#                    return 'No Garden'
#         except:
#              return "No info"

#     garden_area()
#     def number_of_facades():
#         property_dict = Raw_data_InDict["property"]['building']
#         try:
#             for key in property_dict.keys():

#                 if key == 'facadeCount' and property_dict[key] != None:
#                    return property_dict[key]

#                 if key == 'facadeCount' and property_dict[key] == None:
#                    return None
#         except:
#              return "no info"

#     number_of_facades()

#     def swimming_pool():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'hasSwimmingPool' and property_dict[key]==True:
#                    return "Yes"

#                 else:
#                    return  "No"
#         except:
#              return "No info"
#     swimming_pool()

#     def open_fire():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'fireplaceCount' and property_dict[key] == True:
#                    return "Yes"

#                 if key == 'fireplaceCount' and property_dict[key] == None:
#                    return "No"
#         except:
#             return "No info"
#     open_fire()


#     def type_of_transaction():
#         property_dict = Raw_data_InDict["transaction"]
#         # print(property_dict)
#         try:
#             for key in property_dict.keys():
#              # print(key)
#              if key == 'type' and property_dict[key] != None:
#                    return property_dict[key]

#              if key == 'type' and property_dict[key] == None:
#                    return None
#         except:
#              return "No info"

#     type_of_transaction()

#     def  State_of_the_building():
#         property_dict = Raw_data_InDict["property"]["building"]
#         # print(property_dict)
#         try:
#             for key in property_dict.keys():
#              # print(key)
#              if key == "condition" and property_dict[key] != None:
#                    return property_dict[key]

#              if key == "condition" and property_dict[key] == None:
#                    return None
#         except:
#              return "No info"

#     State_of_the_building()


#     def type():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'type':
#                    return (property_dict[key])

#                 if key == 'type' and property_dict[key] == None:
#                    return None
#         except:
#              return "No info"
#     type()


#     def subtype():
#         property_dict = (Raw_data_InDict["property"])
#         try:
#             for key in property_dict.keys():
#                 if key == 'subtype':
#                    return property_dict[key]

#                 if key == 'subtype' and property_dict[key] == None:
#                    return None
#         except:
#              return "No info"
#     subtype()


#     def surface_of_the_land():
#         property_dict = (Raw_data_InDict["property"]['land'])
#         try:
#             for key in property_dict.keys():
#                 if key == 'surface'and property_dict[key] != None:
#                    return property_dict[key]

#                 if key == 'surface' and property_dict[key] == None:
#                    return None
#         except:
#              return "No info"
#     surface_of_the_land()

#     def surface_area_of_the_plot_of_land():
#         property_dict_land = Raw_data_InDict["property"]['land']
#         try:
#          for key1 in property_dict_land.keys():
#           if key1 == 'surface' and property_dict_land[key1] != None:
#             #print(property_dict_land['surface'])
#             break
#          property_dict = (Raw_data_InDict["property"])
#          for key2 in property_dict.keys():
#           if (key2 == 'netHabitableSurface' and property_dict['netHabitableSurface'] != None):
#             #print( property_dict['netHabitableSurface'])
#             break
#          surface_area_of_the_plot_of_land= property_dict_land['surface'] - property_dict['netHabitableSurface']
#          return surface_area_of_the_plot_of_land
#         except:
#              return "No info"
#     surface_area_of_the_plot_of_land()
#     def id():
#        try:
#           for i in Raw_data_InDict.keys():
#              # print(i)
#              if i =='id':
#                if Raw_data_InDict["id"] !=None:
#                 return Raw_data_InDict["id"]
#              else:
#                 return None
#        except:
#          return "No info"


#     def AllInDictionary():
#        a={"id":id(),"Locality": locality(),"Postcode":postcode(), "Street":street(),"Number":property_number(),"Type of property": type(),"Subtype of property":subtype(), "Price": price(),
#        "Type of sale":type_of_transaction(),"Number of rooms":number_of_rooms(), "Living Area":living_area(),"Fully equipped kitchen":kitchen(),
#        "Furnished":furnished(), "Open fire" :open_fire(), "Terrace":terrace(),"TerraceArea" : terrace_area(),
#        "Garden":garden(),"Garden area" :garden_area(),"Surface of the land":surface_of_the_land(),"Surface area of the plot of land"
#        : surface_area_of_the_plot_of_land(),"Number of facades": number_of_facades(), " Swimming pool": swimming_pool(),"State of the building":State_of_the_building()}
#        # print(a)
#        list_all_dict.append(a)
#     AllInDictionary()
# print(list_all_dict)
# df = pandas.DataFrame(list_all_dict)
# df.to_csv('E:\\immo_eliza_scrapping_group7\\file1.csv')

