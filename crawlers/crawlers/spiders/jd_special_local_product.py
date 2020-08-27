import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem

class JdSpecialLocalProductSpider(CrawlSpider):
    name = 'jd-special-local-product'
    allowed_domains = ['jd.com']
    start_urls = ['http://list.jd.com/1320-6559-6561-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6562-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6563-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6564-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6565-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6566-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6567-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1320-6559-6568-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html']

    rules = (
        Rule(LinkExtractor(allow=r'item\.jd\.com/'), callback='parse_item', follow=False),
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

