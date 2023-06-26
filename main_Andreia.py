import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&priceType=SALE_PRICE&page=1&orderBy=relevance"
range_links = range(1, 12)

req = requests.get(root_url)

# Getting the cookies
cookies = req.cookies.get_dict()
#print(cookies)
#print(req.status_code)

def get_links():
    '''Function to find all the links '''
    s = requests.Session()
    req = requests.get(root_url)
    soup = BeautifulSoup(req.text, "html.parser")
    
    links = []
    for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
       links.append(elem.get("href"))
    links = links[0:30]
    
    new_links = []
    for num in root_url:
        if num.isnumeric():
            num = int(num)
            while num < 12:
                num += 1
                print(f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&priceType=SALE_PRICE&page={num}&orderBy=relevance")
    

def scrapping_general():
    link_immo = "https://www.immoweb.be/en/classified/house/for-sale/libin/6890/10657263"
    r = requests.get(link_immo)
    
    s = requests.Session()
    soup = BeautifulSoup(r.text, "html.parser")
    
    for elem in soup.find_all("td", attrs={"class": "classified-table__data"}):
        print(elem.get(""))
    
scrapping_general()
    


