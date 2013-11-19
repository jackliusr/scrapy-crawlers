from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawlers.items import SexauerItem

import urlparse
 
class SexauerSpider(CrawlSpider):
    name = 'sexauer'
    allowed_domains = ['sexauer.com']
    start_urls = ['http://www.sexauer.com/Search/TOOLS/ACCESS-EQUIPMENT']

    rules = (        
        #Rule(SgmlLinkExtractor(allow=['/Search/APPLIANCES'], restrict_xpaths =('//div[@id="new-content-container"]')), callback='parse_cat', follow=True),
        Rule(SgmlLinkExtractor(allow=['&page=']), callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(allow=['/Sku/',]), callback='parse_item', follow=False)
    )
    def parse_cat(self, response):
      pass;
    
    
    def parse_page(self, response):
      pass
    
    
    def parse_item(self, response):
        hxs = Selector(response)
        i = SexauerItem()
        url = response.url       
        i['name'] = hxs.xpath('//h2/strong/text()').extract()
        i['sku'] = url[url.rfind('/') + 1:]
        i['description'] = hxs.xpath('//div[@id="pdc"]').extract()        
        imgurl = hxs.xpath('//div[@id="first"]//div[@id="lightbox_product_picture_inner"]/img/@src').extract()[0]
        absurl = urlparse.urljoin(response.url, imgurl.strip())
        i['image_urls'] = [absurl]
        return i
