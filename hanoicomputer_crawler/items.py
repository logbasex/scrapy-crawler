# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HanoicomputerCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    product_name = scrapy.Field()
    product_code = scrapy.Field()
    price = scrapy.Field()

    pass
