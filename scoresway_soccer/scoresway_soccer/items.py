# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScoreswaySoccerItem(scrapy.Item):
    # define the fields for your item here like:
    tournament_url = scrapy.Field()
    name = scrapy.Field()
    season_url = scrapy.Field()
    logos = scrapy.Field()
    pass
