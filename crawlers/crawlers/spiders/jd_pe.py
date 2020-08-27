from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem

class JdPeSpider(CrawlSpider):
    name = 'jd-pe'
    allowed_domains = ['jd.com']
    start_urls = ['http://list.jd.com/1318-1466-1695-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-1694-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-1698-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-1697-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-1696-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-1699-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-1700-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',
          'http://list.jd.com/1318-1466-5155-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html',]

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
