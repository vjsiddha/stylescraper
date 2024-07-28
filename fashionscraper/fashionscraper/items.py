import scrapy
from scrapy.item import Item, Field

class FashionItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class EcommerceScraperItem(scrapy.Item):
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    product_details = scrapy.Field()
    additional_details = scrapy.Field()
    product_link = scrapy.Field()
    source = scrapy.Field()
    image_urls = scrapy.Field()