import scrapy

class FashionItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
