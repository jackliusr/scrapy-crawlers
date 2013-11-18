# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlersItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class SchoolItem(Item):
  name = Field()
  phone = Field()
  fax = Field()
  email = Field()
  address = Field()
  principal = Field()
  
  
  
