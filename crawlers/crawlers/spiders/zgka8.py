from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from crawlers.items import Zgka8Item
from scrapy.http import TextResponse,FormRequest,Request
import json
from scrapy import log

class Zgka8Spider(CrawlSpider):
    name = 'zgka8'
    allowed_domains = ['zgka8.com']
    start_urls = ['http://www.zgka8.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'http://www.zgka8.com/category.php\?id='), callback='parse_cat', follow=True),
        Rule(SgmlLinkExtractor(allow=r'http://www.zgka8.com/goods.php\?id='), callback='parse_good', follow=False),
    )

    def parse_cat(self, response):
       pass
      
    def parse_good(self, response):
	sel = Selector(response)
	i = Zgka8Item()
	url = response.url
	#productId = url[-3:]
	#i['productId'] = productId
	i['name'] = sel.xpath("//div[@class='goodsCenter']/h1/text()").extract()
	i['description'] =' '.join(sel.xpath("//div[@id='goods_h']/blockquote/p").extract())
	i['category'] = sel.xpath("//div[@class='ur_1']/a[2]/text()").extract()
	i['price'] = sel.xpath("//span[@id='ECS_SHOPPRICE']/text()").extract()
	i['image_urls'] = ["http://www.zgka8.com/" + sel.xpath("//div[@class='goodImg']/a/img/@src").extract()[0]]
	return i;