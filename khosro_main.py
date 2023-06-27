import requests
from bs4 import BeautifulSoup
url="https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"
req= requests.get(url)
print(req.status_code)
soup= BeautifulSoup(req.text, "html.parser")
import json
import re
data = soup.find('div',attrs={"class":"container-main-content"}).script.text
print(data)
#print(data)
#.result = soup.find("script", string=lambda t: "window.dataLayer" in t).string # Script element
test= re.findall(r"window.classified = (\{.*\})", data)
result = json.loads(test[0]) # Data dictionary 
print(result)
# # a=(data[0]['classified'])  

# # # print(data)
# # data[0]['price']
# # # for i in a:
# # #     if i=="price":
# # #      print(i+1)
     
        
    
        
       
       
    
# number_properties = 
# page_links=[]

# for i in url:



#     page_links.append
# links=[]

# elem=soup.find("a", attrs={"class":"card_title-link"})
#     # elem=elem.get("href")
# print(elem)
#     links.append(elem)
 
# #print(links[0:30])

    



# each_properties_url= "https://www.immoweb.be/en/classified/house/for-sale/lede/9340/10660142"     
# req_each_properties= requests.get(each_properties_url)
# # print(req_each_properties.status_code)
# soup= BeautifulSoup(req_each_properties.text, "html.parser")
# # interior=soup.find("h2", attrs={"class":"text-block__title"})
# living_area=soup.find_all("td", attrs={"class":"classified-table__data"})[7]
# import re
# living_area=re.sub(" " ,"", str(living_area))
# living_area=re.findall("\d{1,10}",living_area)
# print(living_area)






