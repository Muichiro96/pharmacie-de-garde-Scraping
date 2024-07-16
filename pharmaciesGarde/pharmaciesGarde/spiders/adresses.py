import scrapy
import json

class AdressesSpider(scrapy.Spider):
    name = "adresses"
    allowed_domains = ["www.annuaire-gratuit.ma"]
    with open('..\Data\pharmacies.json',encoding="utf8") as file:
        data = json.load(file)
    start_urls = [f"https://www.annuaire-gratuit.ma{pharmacie['url']}" for pharmacie in data]
   
  
        

    def parse(self, response):
        yield{
            'adresse' : response.css("address").xpath(".//text()").get(),
            'lat&long': response.css("address").xpath(".//a/@href").get().replace("https://maps.google.com/maps?q=","")
        }
        
        
              

