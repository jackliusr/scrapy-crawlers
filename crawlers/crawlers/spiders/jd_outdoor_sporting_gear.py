import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem

class JdOutdoorSportingGearSpider(CrawlSpider):
    name = 'jd-outdoor-sporting-gear'
    allowed_domains = ['jd.com']
    start_urls = ['http://list.jd.com/1318-1462-1473-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-1474-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-1475-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-1472-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-1476-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-2630-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-2631-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1462-1479-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html']

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
