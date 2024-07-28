import scrapy
from fashionscraper.items import FashionItem

class FashionSpider(scrapy.Spider):
    name = "fashion"
    start_urls = [
        'https://www2.hm.com/en_us/men/products/jeans.html',
        'https://www2.hm.com/en_us/women/new-arrivals/view-all.html',
        'https://www2.hm.com/en_us/men/new-arrivals/view-all.html',
        'https://www2.hm.com/en_ca/men/shop-by-product/view-all.html',
        'https://www2.hm.com/en_ca/women/shop-by-product/view-all.html',
    ]

    def parse(self, response):
        self.log(f"Visited {response.url}")
        for item in response.css('article'):
            # Filter out promotional articles
            if 'data-articlecode' not in item.attrib:
                continue

            name = item.css('h2::text').get()
            if name:
                name = name.strip()
            else:
                self.log(f"Name not found in: {item}")

            price = item.css('span.aeecde.ac3d9e.b19650::text').get()
            if price:
                price = price.strip()
            else:
                self.log(f"Price not found in: {item}")

            link = item.css('a::attr(href)').get()
            if link:
                link = response.urljoin(link)
            else:
                self.log(f"Link not found in: {item}")

            # Extract the best resolution image from srcset
            srcset = item.css('img::attr(srcset)').get()
            if srcset:
                image = self.extract_highest_res_image(srcset)
            else:
                image = item.css('img::attr(src)').get()
                if not image:
                    self.log(f"Image not found in: {item}")

            if name and price and link and image:
                yield {
                    'name': name,
                    'price': price,
                    'link': link,
                    'image_urls': [image],  # Make sure this is a list
                }

    def extract_highest_res_image(self, srcset):
        # Extract the highest resolution image URL from the srcset attribute
        image_urls = srcset.split(',')
        highest_res_url = ''
        highest_res = 0
        for url in image_urls:
            parts = url.strip().split(' ')
            if len(parts) > 1:  # Ensure there is a resolution part
                res = int(parts[1][:-1])
                if res > highest_res:
                    highest_res = res
                    highest_res_url = parts[0]
        return highest_res_url
