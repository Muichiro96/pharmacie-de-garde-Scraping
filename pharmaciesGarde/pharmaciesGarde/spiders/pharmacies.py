import scrapy


class PharmaciesSpider(scrapy.Spider):
    name = "pharmacies"
    allowed_domains = ["www.annuaire-gratuit.ma"]
    start_urls = ["https://www.annuaire-gratuit.ma/pharmacies"]
    
    def parse(self, response):
        pharmacies = response.css("li[itemprop='itemListElement']")
        
        for pharmacie in pharmacies:
           
            yield {
                'nom' : pharmacie.xpath(".//h3[@itemprop='name']/text()").get(),
                'ville':pharmacie.xpath(".//span[@itemprop='addressRegion']/text()").get(),
                'telephone': pharmacie.xpath(".//span[@itemprop='telephone']/text()").get(),
                    'description':pharmacie.xpath(".//p[@itemprop='description']/text()").get(),
                    'url': pharmacie.xpath(".//a[@itemprop='url']/@href").get()
             } 
        nextPage = response.css('a[class="page-link pagination__next"]::attr(href)').get()
        if nextPage:
            next_url = f"https://www.annuaire-gratuit.ma{nextPage}"
            yield scrapy.Request( 
                url = next_url, 
                callback = self.parse 
            ) 
        
       