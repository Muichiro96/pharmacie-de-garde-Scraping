import scrapy


class FulladressSpider(scrapy.Spider):
    name = "FullAdress"
    allowed_domains = ["annuaire-gratuit.ma"]
    start_urls = ["https://annuaire-gratuit.ma"]

    def parse(self, response):
        pass
