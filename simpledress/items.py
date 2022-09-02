# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class SimpledressItem(scrapy.Item):
    title= scrapy.Field()
    Image_URL = scrapy.Field()
    Current_price= scrapy.Field()
    old_price = scrapy.Field()
    price = scrapy.Field()
    size_options = scrapy.Field()
    Color = scrapy.Field()
