from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import GameItem
from scrapy.http import TextResponse,FormRequest,Request
import json

class ChangyoucardSpider(CrawlSpider):
    name = 'changyoucard'
    allowed_domains = ['changyoucard.com']
    start_urls = ['http://www.changyoucard.com/category-197-b0.html',
          'http://www.changyoucard.com/category-550-b0.html',
          'http://www.changyoucard.com/category-418-b0.html',
          'http://www.changyoucard.com/category-412-b0.html',
          'http://www.changyoucard.com/category-489-b0.html',
          'http://www.changyoucard.com/category-488-b0.html',
          'http://www.changyoucard.com/category-487-b0.html',
          'http://www.changyoucard.com/category-486-b0.html']

    rules = (
        Rule(LinkExtractor(allow=r'goods-'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
      sel = Selector(response)
      i = GameItem()
      i['name'] = sel.xpath('//div[@class="imgInfo"]/a/img/@alt').extract()[0]
      i['description'] = sel.xpath('//div[@class="imgInfo"]/a/img/@alt').extract()[0]
      i['category'] = sel.xpath('//div[@id="ur_here"]/a[2]/text()').extract()[0]
      i['price'] = sel.xpath("//font[@id='ECS_SHOPPRICE']/text()").extract()[0]
      i['image_urls'] = ["http://www.changyoucard.com/" +  sel.xpath('//div[@class="imgInfo"]/a/img/@src').extract()[0]]
      return i;
