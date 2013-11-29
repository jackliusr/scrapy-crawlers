from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawlers.items import JdItem

class JdEmergencyHealthSpider(CrawlSpider):
    name = 'jd-emergency-health'
    allowed_domains = ['jd.com']
    start_urls = ['http://list.jd.com/1318-1469-1514-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1318-1469-1515-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1318-1469-1516-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1318-1469-1517-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',		  
		  'http://list.jd.com/1318-1469-1518-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1318-1469-1519-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1318-1469-1520-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1318-1469-1521-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html']

    rules = (
	Rule(SgmlLinkExtractor(allow=r'item\.jd\.com/'), callback='parse_item', follow=False),
    )


    def parse_item(self, response):
	sel = Selector(response)
        i = JdItem()
        i['name'] = sel.xpath("//div[@id='name']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@id='product-detail-1']/ul").extract()
        i['category'] = sel.xpath("//div[@class='breadcrumb']/span/a/text()").extract()[1]
        i['price'] = sel.xpath("//strong[@id='jd-price']/text()").extract()
        i['image_urls'] = sel.xpath("//div[@id='spec-n1']/img/@src").extract()
        return i