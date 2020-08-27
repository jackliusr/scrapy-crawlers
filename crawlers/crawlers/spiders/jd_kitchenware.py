import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem
from scrapy.http import TextResponse,FormRequest,Request
import json

class JdKitchenwareSpider(CrawlSpider):
    name = 'jd-kitchenware'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['http://list.jd.com/6196-6197-6199-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6200-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6201-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6202-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6203-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6204-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6205-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6206-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/6196-6197-6208-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html']

    rules = (
    Rule(LinkExtractor(allow=r'item\.jd\.com/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):      
        sel = Selector(response)
        i = JdItem()
        i['name'] = sel.xpath("//div[@id='name']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@id='product-detail-1']/ul").extract()
        i['category'] = sel.xpath("//div[@class='breadcrumb']/span/a/text()").extract()[1]
        #i['price'] = sel.xpath("//strong[@id='jd-price']/text()").extract()
        i['image_urls'] = sel.xpath("//div[@id='spec-n1']/img/@src").extract()
        url = response.url
        itemid = url[url.rindex('/')+1:-5]   
        request=  Request("http://p.3.cn/prices/get?skuid=J_%s&type=1" % itemid, callback=self.parse_price)
        request.meta['item'] = i
        yield request
        
    def parse_price(self, response):
      i = response.meta['item']
      jsonData = json.loads(response.body)
      #i['itemid'] = jsonData[0]['id']
      i['price'] = jsonData[0]['p']
      return i
