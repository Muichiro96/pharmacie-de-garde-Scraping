import scrapy
import json

class AdressesSpider(scrapy.Spider):
    name = "adresses"
    allowed_domains = ["www.annuaire-gratuit.ma"]
    with open('..\Data\pharmacies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    custom_settings = {
    'CONCURRENT_REQUESTS': 1  
    }
   
    start_urls= [f"https://www.annuaire-gratuit.ma{pharmacie['url']}"  for pharmacie in data]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
  
    def handle_failure(self, failure):
        self.log(failure, level=logging.ERROR)
    
        self.log('restart from the failed url {}'.format(failure.request.url))
        yield scrapy.Request(
            url=failure.request.url,
            callback=self.parse,
            errback=self.handle_failure)   

    def parse(self, response):
        yield{
            'adresse' : response.css("address").xpath(".//text()").get(),
            'lat&long': response.css("address").xpath(".//a/@href").get().replace("https://maps.google.com/maps?q=","")
        }
        
        
              

