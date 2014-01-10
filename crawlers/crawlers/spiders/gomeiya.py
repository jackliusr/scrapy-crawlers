from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from crawlers.items import GomeiyaItem
from scrapy.http import TextResponse,FormRequest,Request
import json
from scrapy import log
class GomeiyaSpider(CrawlSpider):
    name = 'gomeiya'
    allowed_domains = ['gomeiya.com']
    start_urls = ['http://www.gomeiya.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'category-.*.html'), callback='parse_cat', follow=True),
        Rule(SgmlLinkExtractor(allow=r'goods-\d*.html'), callback='parse_good', follow=False),
    )

    def parse_cat(self, response):
       pass
      
    def parse_good(self, response):
	sel = Selector(response)
	i = GomeiyaItem()
	url = response.url
	#productId = url[-3:]
	#i['productId'] = productId
	i['name'] = sel.xpath("//div[@id='container']/div[2]/div[1]/div/text()").extract()[0]
	i['description'] = ' '.join(sel.xpath("//div[@class='content-div']/div/div/div/div/div[1]/*").extract())
	i['category'] = sel.xpath("//div[@id='wrapper']/div[6]/a[2]/text()").extract()[0]
	i['price'] = sel.xpath("//span[@id='ECS_RANKPRICE_1']/text()").extract()
	i['image_urls'] =["http://www.gomeiya.com/" +  sel.xpath("//div[@class='wap-right']/div/table//td[1]/div/a/img/@src").extract()[0]]
	return i;