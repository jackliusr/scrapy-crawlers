import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem
from scrapy.http import TextResponse,FormRequest,Request
import json

class JdHardwareSpider(scrapy.Spider):
    name = 'jd-hardware'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['http://list.jd.com/737-1277-934-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-3979-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-6974-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-900-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-1295-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-6975-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-4934-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/737-1277-5004-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html'
         ]

    def parse(self,response):
      sel = Selector(response)
      urls = sel.xpath("//a[contains(@href, 'item.jd.com/')]/@href").extract()
      for url in urls:
         itemid = url[url.rindex('/')+1:-5]
         yield Request(url, callback=self.parse_item)   
      
    def parse_item(self, response):      
        sel = Selector(response)
        i = JdItem()
        url = response.url
        itemid = url[url.rindex('/')+1:-5]        
        i['name'] = sel.xpath("//div[@id='name']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@id='product-detail-1']/ul").extract()
        i['category'] = sel.xpath("//div[@class='breadcrumb']/span/a/text()").extract()[1]
        i['image_urls'] = sel.xpath("//div[@id='spec-n1']/img/@src").extract()      
        request=  Request("http://p.3.cn/prices/get?skuid=J_%s&type=1" % itemid, callback=self.parse_price)
        request.meta['item'] = i
        yield request
        
    def parse_price(self, response):
        i = response.meta['item']
        jsonData = json.loads(response.body)    
        i['price'] = jsonData[0]['p']
        return i

        
      
