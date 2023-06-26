from bs4 import BeautifulSoup
import requests

def get_links():
    """
    Function that gets links of all houses
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
    """
    Function to get data of individual houses
    """
get_links()

