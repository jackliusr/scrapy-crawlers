from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import HezigameItem
from scrapy.http import TextResponse,FormRequest,Request
import json

class HezigameSpider(CrawlSpider):
    name = 'hezigame'
    allowed_domains = ['hezigame.com']
    start_urls = ['http://www.hezigame.com/']

    rules = (
        Rule(LinkExtractor(allow=r'category.php\?id='), callback='parse_cat', follow=True),
        Rule(LinkExtractor(allow=r'goods.php\?id='), callback='parse_good', follow=False)
    )

    def parse_cat(self, response):
       pass
      
    def parse_good(self, response):
      sel = Selector(response)
      i = HezigameItem()
      url = response.url
      #productId = url[-3:]
      #i['productId'] = productId
      i['name'] = sel.xpath("//h2[@class='name']/text()").extract()[0]
      i['description'] = sel.xpath("//ul[@class='line']/li[1]/text()").extract()[0]
      i['category'] = sel.xpath("//div[@id='urHere']/h3/a[2]/text()").extract()[0]
      i['price'] = sel.xpath("//span[@id='ECS_SHOPPRICE']/text()").extract()
      i['image_urls'] =["http://www.hezigame.com/" +  sel.xpath("//div[@id='itemPic']/a/img/@src").extract()[0]]
      return i;
