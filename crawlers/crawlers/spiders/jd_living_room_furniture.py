import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem

class JdLivingRoomFurnitureSpider(CrawlSpider):
    name = 'jd-living-room-furniture'
    allowed_domains = ['jd.com']
    start_urls = ['http://list.jd.com/9847-9849-9870-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-9871-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-9872-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-9873-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-9874-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-9875-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-9876-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html',
          'http://list.jd.com/9847-9849-11142-0-0-0-0-0-0-0-1-1-1-1-21-1827-3505-0.html']

    rules = (
        Rule(LinkExtractor(allow=r'item\.jd\.com/'), callback='parse_item', follow=False,process_request= 'process_request'),
    )

    def process_request(self, request):
      request.meta['renderjs'] = 1
      return request
    
    def parse_item(self, response):
        sel = Selector(response)
        i = JdItem()
        i['name'] = sel.xpath("//div[@id='name']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@id='product-detail-1']/ul").extract()
        i['category'] = sel.xpath("//div[@class='breadcrumb']/span/a/text()").extract()[1]
        i['price'] = sel.xpath("//strong[@id='jd-price']/text()").extract()
        i['image_urls'] = sel.xpath("//div[@id='spec-n1']/img/@src").extract()
        return i
