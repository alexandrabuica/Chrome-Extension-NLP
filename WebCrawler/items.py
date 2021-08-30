# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewspapercrawlerItem(scrapy.Item): 
    titlu = scrapy.Field()
    sursa = scrapy.Field()
    corp = scrapy.Field()
    rezumat = scrapy.Field()
    imagine = scrapy.Field() 
    pass
