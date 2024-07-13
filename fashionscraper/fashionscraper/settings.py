import os

BOT_NAME = "fashionscraper"

SPIDER_MODULES = ["fashionscraper.spiders"]
NEWSPIDER_MODULE = "fashionscraper.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Ensure this is correct
FEED_FORMAT = "json"
FEED_URI = os.path.join(os.path.dirname(__file__), "items.json")
