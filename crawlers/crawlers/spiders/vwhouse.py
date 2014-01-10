from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from crawlers.items import VwhouseItem
from scrapy.http import TextResponse,FormRequest,Request
import json
from scrapy import log

class VwhouseSpider(CrawlSpider):
    name = 'vwhouse'
    allowed_domains = ['vwhouse.com']
    #start_urls = ['http://www.vwhouse.com/']

    start_urls = ['http://www.vwhouse.com/category-2-b0.html',
		  'http://www.vwhouse.com/category-3-b0.html',
		  'http://www.vwhouse.com/category-4-b0.html',
		  'http://www.vwhouse.com/category-5-b0.html',
		  'http://www.vwhouse.com/category-16-b0.html',
		  'http://www.vwhouse.com/category-18-b0.html',
		  'http://www.vwhouse.com/category-19-b0.html',
		  'http://www.vwhouse.com/category-20-b0.html',
		  'http://www.vwhouse.com/category-24-b0.html',
		  'http://www.vwhouse.com/category-29-b0.html',
		  'http://www.vwhouse.com/category-47-b0.html',
		  'http://www.vwhouse.com/category-62-b0.html']

    rules = (
	Rule(SgmlLinkExtractor(allow=r'goods-\d+\.html'), callback='parse_item', follow=False),
    )
      
    def parse_item(self, response):
	sel = Selector(response)
	i = VwhouseItem()
	i['name'] = sel.xpath("//div[@id='goodsInfo']/div[@class='textInfo']/form/p/text()").extract()[0]
	i['description'] =' '.join(sel.xpath("//div[@id='com_h']/blockquote/p/span/*").extract())
	i['category'] = sel.xpath("//div[@id='ur_here']/a[3]/text()").extract()[0]
	i['price'] = sel.xpath("//font[@id='ECS_SHOPPRICE']/text()").extract()[0]
	i['image_urls'] = ["http://www.vwhouse.com/" +  sel.xpath("//div[@class='imgInfo']/img/@src").extract()[0]]
	return i;
