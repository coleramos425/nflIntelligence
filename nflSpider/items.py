import scrapy

class PlayerItem(scrapy.Item):
    number = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    age = scrapy.Field()
    team = scrapy.Field()
    stats = scrapy.Field()
