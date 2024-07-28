import scrapy
from fashionscraper.items import FashionItem
import random

class NordstromSpider(scrapy.Spider):
    name = "nordstrom"
    start_urls = [
        'https://www.nordstrom.com/browse/women/clothing',
        'https://www.nordstrom.com/browse/men/clothing',
        'https://www.nordstrom.com/browse/kids/girls-clothing',
        'https://www.nordstrom.com/browse/kids/boys-clothing',
        'https://www.nordstrom.com/browse/home'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': random.uniform(1, 3),  # Random delay between 1 to 3 seconds
    }

    def parse(self, response):
        self.log(f"Visited {response.url}")
        for item in response.css('article[class^="zzWFq RpUx3"]'):
            name = item.css('h3[class^="kKGYj Y9bA4"] a::text').get()
            if name:
                name = name.strip()
            else:
                self.log(f"Name not found in: {item}")

            price = item.css('div[class^="NMGaP UuGnV"] span[class^="ZZpS1"]::text').get()
            if price:
                price = price.strip()
            else:
                self.log(f"Price not found in: {item}")

            link = item.css('h3[class^="kKGYj Y9bA4"] a::attr(href)').get()
            if link:
                link = response.urljoin(link)
            else:
                self.log(f"Link not found in: {item}")

            image = item.css('img::attr(src)').get()
            if not image:
                self.log(f"Image not found in: {item}")

            if name and price and link and image:
                yield FashionItem(
                    name=name,
                    price=price,
                    link=link,
                    image_urls=[image],
                )
            else:
                self.log(f"Incomplete item data: name={name}, price={price}, link={link}, image={image}")

# Remember to run this spider using the command:
# scrapy crawl nordstrom
