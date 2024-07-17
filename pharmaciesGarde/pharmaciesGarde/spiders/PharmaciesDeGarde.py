import scrapy
from datetime import date
class PharmaciesdegardeSpider(scrapy.Spider):
    name = "GardeJour"
 
    allowed_domains = ["www.annuaire-gratuit.ma"]
    start_urls = ["https://www.annuaire-gratuit.ma/pharmacie-garde-maroc.html"]

    def parse(self, response):
        list =response.css("li[class*='col-xs-12 ag_listing_item']")
        for ele in list:
            if ele.xpath('.//a/@href').get():    
                list_garde_jour = ele.xpath('.//a/@href').get().replace(".html","/garde-jour.html")
                yield scrapy.Request( 
                    url = f"https://www.annuaire-gratuit.ma{list_garde_jour}", 
                    callback = self.listeParVille 
                ) 


    def listeParVille(self,response):
        list =response.css("li[class*='col-xs-12 ag_listing_item']")
        for element in list:
            url_garde_jour = element.xpath('.//a/@href').get()
            if url_garde_jour:
                yield scrapy.Request( 
                    url = f"https://www.annuaire-gratuit.ma{url_garde_jour}",
                    callback = self.gardeJour
                )
    def gardeJour(self,response):
        yield{
            'nom' : response.css("span[itemprop='name']").xpath(".//text()").get(),
            'ville': response.css("td[itemprop='addressRegion']").xpath(".//text()").get(),
            'telephone': response.css("a[itemprop='telephone']").xpath(".//text()").get(),
            'adresse' : response.css("address").xpath(".//text()").get(),
            'lat&long': response.css("address").xpath(".//a/@href").get().replace("https://maps.google.com/maps?q=",""),
            'date': date.today()
        }
