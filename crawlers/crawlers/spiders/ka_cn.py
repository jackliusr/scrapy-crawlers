from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawlers.items import CardItem
import urlparse

class KaCnSpider(CrawlSpider):
    name = 'ka-cn'
    allowed_domains = ['ka-cn.com']
    start_urls = ['http://www.ka-cn.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=['category-'],restrict_xpaths = ('//div/h3/a')), callback='parse_cat', follow=True),
        Rule(SgmlLinkExtractor(allow=['goods-'], restrict_xpaths =('//form/div/ul/li')), callback='parse_good',follow=True),        
        )

    def parse_cat(self, response):
	pass
   
    def parse_good(self, response):
        hxs = Selector(response)
        i = CardItem()
        i["name"] = hxs.xpath("//div[@id='goodsInfo_text']/form/div/p[@class='f_l']/text()").extract()
        i["price"] = hxs.xpath("//font[@id='ECS_SHOPPRICE']/text()").extract()       
        i["description"] = hxs.xpath("//blockquote").extract()[0]        
        imgurl = hxs.xpath('//div[@id="goodsInfo_img"]/div/a/img/@src').extract()[0]
        absurl = urlparse.urljoin(response.url, imgurl.strip())
        i['image_urls'] = [absurl]
        return i
