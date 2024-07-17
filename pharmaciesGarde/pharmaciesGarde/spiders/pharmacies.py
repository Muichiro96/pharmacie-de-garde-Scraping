import scrapy


class PharmaciesSpider(scrapy.Spider):
    name = "pharmacies"
    allowed_domains = ["www.annuaire-gratuit.ma"]
    start_urls = ["https://www.annuaire-gratuit.ma/pharmacies"]
   
  
    
    def parse(self, response):
        pharmacies = response.css("li[itemprop='itemListElement']")
        
        for pharmacie in pharmacies:
            pharmacieURL=pharmacie.xpath(".//a[@itemprop='url']/@href").get()
            yield scrapy.Request( 
                url = f"https://www.annuaire-gratuit.ma{pharmacieURL}", 
                callback = self.data_collect 
            ) 
            
        nextPage = response.css('a[class="page-link pagination__next"]::attr(href)').get()
        if nextPage:
            next_url = f"https://www.annuaire-gratuit.ma{nextPage}"
            yield scrapy.Request( 
                url = next_url, 
                callback = self.parse 
            ) 
    def data_collect(self,response):
        yield{
            'nom' : response.css("span[itemprop='name']").xpath(".//text()").get(),
            'ville': response.css("td[itemprop='addressRegion']").xpath(".//text()").get(),
            'telephone': response.css("a[itemprop='telephone']").xpath(".//text()").get(),
            'adresse' : response.css("address").xpath(".//text()").get(),
            'lat&long': response.css("address").xpath(".//a/@href").get().replace("https://maps.google.com/maps?q=","")

        }
        
       