from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawlers.items import JdItem
from selenium import selenium

class JdChildrenClothersSpider(CrawlSpider):
    name = 'jd-children-clothers'
    allowed_domains = ['jd.com']
    start_urls = ['http://list.jd.com/1315-3961-11222-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-11223-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-11224-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-11225-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-11227-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-11226-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-4937-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
		  'http://list.jd.com/1315-3961-3977-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'item\.jd\.com/'), callback='parse_item', follow=False),
    )

    def __init__(self):
      CrawlSpider.__init__(self)
      self.verificationErrors = []
      self.selenium = selenium("localhost", 4444, "*firefox", "http://www.jd.com")
      self.selenium.start()
      
    def __del__(self):
	self.selenium.stop()
	print self.verificationErrors
	CrawlSpider.__del__(self)
	
    def parse_item(self, response):
        sel = Selector(response)
        i = JdItem()
        
        i['name'] = sel.xpath("//div[@id='name']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@id='product-detail-1']/ul").extract()
        i['category'] = sel.xpath("//div[@class='breadcrumb']/span/a/text()").extract()[2]
        i['image_urls'] = sel.xpath("//div[@id='spec-n1']/img/@src").extract()
        
        #Do some crawling of javascript created content with Selenium
        selr = self.selenium
	selr.open(response.url)
	#Wait for javscript to load in Selenium
	selr.wait_for_page_to_load(10000)
        i['price'] = selr.get_text("identifier=jd-price")
        return i
