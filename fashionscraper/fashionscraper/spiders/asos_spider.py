import scrapy
from fashionscraper.items import EcommerceScraperItem
from scrapy.http import Request
import re

class AsosEcommerceSpider(scrapy.Spider):
    name = 'asos'

    def start_requests(self):
        # List of URLs to scrape
        urls = [
            'https://www.asos.com/us/men/new-in/cat/?cid=27110'
        ]

        for url in urls:
            yield scrapy.Request(url=url, meta={'gender': 'men', 'category': 'new-in'}, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"STARTING URL: {response.request.url}")
        gender = response.meta['gender']
        category = response.meta['category']
        
        # Adjust the XPath expression as per the current structure
        text_list = response.xpath('//p[@class="styleCount_xO2zS"]/text()').extract()

        if not text_list:
            self.logger.error("No text found for XPath expression '//p[@class=\"styleCount_xO2zS\"]/text()'")
            return

        text = text_list[0]
        self.logger.info(text)

        try:
            total = int(re.findall(r'\d+', text)[0])
            per_page = len(response.xpath('//article[@class="productTile_U0clN"]'))
            num_pages = round(total / per_page)
        except:
            self.logger.error("Failed to extract pagination information")
            return

        link_urls = [response.request.url + '&page={}'.format(i) for i in range(1, num_pages + 1)]
        for link_url in link_urls:
            self.logger.info(f"DOING URL {link_url}")
            yield Request(link_url, meta={'gender': gender, 'category': category}, callback=self.parse_result_page)

    def parse_result_page(self, response):
        products = response.xpath('//article[@class="productTile_U0clN"]')
        gender = response.meta['gender']
        category = response.meta['category']
        self.logger.info(f'Number of products is {len(products)}')
        for product in products:
            detail_url = product.xpath('.//@href').extract_first()  # We are looking for url of the detail page.
            price = product.xpath('.//p/span[2]/text()').extract_first()
            yield Request(url=detail_url, meta={'price': price, 'product_link': detail_url, 'gender': gender, 'category': category}, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        product_id = response.xpath('//div[@class="product-code"]/p/text()').extract_first()
        product_name = response.xpath('//div[@class="product-hero"]/h1/text()').extract_first()

        product_details = response.xpath('//div[@class="product-description"]/ul/li/text()').extract()
        additional_details = response.xpath('//div[@class="about-me"]/text()').extract()

        image_urls = []
        image_urls = [image.replace('$S$', '$XXL$').replace('wid=40', 'wid=513') for image in response.xpath('//*/img/@src').extract() if 'product' in image]
        
        # Save results
        item = EcommerceScraperItem()

        item['product_id'] = product_id
        item['product_name'] = product_name
        item['category'] = response.meta['category']
        item['gender'] = response.meta['gender']
        item['price'] = response.meta['price']
        item['brand'] = None

        item['product_details'] = product_details
        item['additional_details'] = additional_details

        item['product_link'] = response.meta['product_link']
        item['source'] = "ASOS"
        item['image_urls'] = image_urls

        yield item
