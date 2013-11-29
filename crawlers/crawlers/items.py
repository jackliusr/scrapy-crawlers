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
  schoolCode = Field()
  schoolType = Field()
  
  
class PrincipalItem(Item):
  schoolCode = Field()
  name = Field()
  
class SexauerItem(Item):
  name = Field()
  sku = Field()
  description = Field()
  image_urls = Field()
  images=Field()
  
  
class CardItem(Item):
    name = Field()
    description = Field()
    price = Field()    
    images = Field()
    image_urls = Field()

class MagazineItem(Item):
  name = Field()
  description = Field()
  category = Field()
  price = Field()
  images = Field()
  image_urls = Field()
  
class JdItem(Item):
  #itemid = Field()
  name = Field()
  description = Field()
  category = Field()
  price = Field()
  images = Field()
  image_urls = Field()

class TaoItem(Item):  
  name = Field()
  description = Field()
  category = Field()
  price = Field()
  images = Field()
  image_urls = Field()


class VsigoItem(Item):
  name = Field()
  description = Field()
  category = Field()
  price = Field()
  images = Field()
  image_urls = Field()


 