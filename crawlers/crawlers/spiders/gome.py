from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import GomeItem
from scrapy.http import TextResponse,FormRequest,Request
import json

class GomeSpider(CrawlSpider):
    name = 'gome'
    allowed_domains = ['gome.com.cn','gomein.net.cn']
    
    #start_urls = ['http://www.gome.com.cn/']
    start_urls = ['http://www.gome.com.cn/category/cat15787588.html',
          'http://www.gome.com.cn/category/cat10000079.html',
          'http://www.gome.com.cn/category/cat10000080.html',
          'http://www.gome.com.cn/category/cat10000078.html',
          'http://www.gome.com.cn/category/cat10000077.html',
          'http://www.gome.com.cn/category/cat10000082.html',
          'http://www.gome.com.cn/category/cat10000089.html',
          'http://www.gome.com.cn/category/cat10000088.html',
          'http://www.gome.com.cn/category/cat10005424.html',
          'http://www.gome.com.cn/category/cat10000086.html',
          'http://www.gome.com.cn/category/cat15787589.html']
    rules = (
        Rule(LinkExtractor(allow=r'http://www\.gome\.com\.cn/product/'), callback='parse_item', follow=False),
    )
  
    def parse_item(self, response):
      sel = Selector(response)
      i = GomeItem()
      i['name'] = sel.xpath("//h1[@class='prdtit']/text()").extract()
      i['description'] = ' '.join(sel.xpath("//ul[@class='specbox']//*").extract())
      i['category'] = sel.xpath("//div[@class='local']/a[3]/text()").extract()[0]
      i['price'] = sel.xpath("//span[@id='prdPrice']/text()").extract()
      i['image_urls'] = sel.xpath("//div[@class='jqzoom']/img/@gome-src").extract()
      return i;
