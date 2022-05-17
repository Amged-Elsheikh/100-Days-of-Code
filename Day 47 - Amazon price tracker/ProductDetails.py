import re
import lxml
import requests
from bs4 import BeautifulSoup


class ProductDetails:
    def __init__(self, url):
        self._id = url
        
        headers = {"Accept-Language":"en-JP,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,ar-JP;q=0.6,ar;q=0.5,en-GB;q=0.4,en-US;q=0.3",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}

        response = requests.get(self._id, headers=headers) 
        response.raise_for_status()
        self._soup = BeautifulSoup(response.content, "lxml")
    

    @property
    def price(self):
        price_string = self._soup.find("span",  class_="a-offscreen").text
        return float(re.sub("[^\d\.]", "", price_string))

    @price.setter
    def price(self, value):
        print("Can't manually set price")

    @property
    def name(self):
        return self._soup.find("span", id="productTitle").text.strip()

    @property
    def price_unit(self):
        return self._soup.find("span", class_="a-price-symbol").text

    @property
    def price_details(self):
        return f"{self.price}{self.price_unit}"

    def get_url(self):
        return self._id
    
    def __repr__(self):
        return f"{self.name}\n\n Price: {self.price_details}"
        
if __name__ == '__main__':
    url = "https://www.amazon.co.jp/-/en/Gaming-Laptop-G513IE-Eclipse-G513IE-R7R30/dp/B09MYYMVQM/?_encoding=UTF8&pd_rd_w=jWYC8&pf_rd_p=baf93712-734c-4342-ae03-33b258824a43&pf_rd_r=880P78RH34XHY1AZ4S05&pd_rd_r=359b9629-571f-4f51-8e65-e4c97d33817b&pd_rd_wg=owTTj&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
    laptop = ProductDetails(url)
    print(laptop)
