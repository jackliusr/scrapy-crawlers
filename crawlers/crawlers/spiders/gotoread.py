from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import MagazineItem

import urllib.parse

class GotoreadSpider(CrawlSpider):
    name = 'gotoread'
    allowed_domains = ['gotoread.com']
    start_urls = ['http://www.gotoread.com/scatalog3687.html',
          'http://www.gotoread.com/scatalog3078.html',
          'http://www.gotoread.com/scatalog3063.html',
          'http://www.gotoread.com/scatalog3010.html',
          'http://www.gotoread.com/scatalog3117.html',
          'http://www.gotoread.com/scatalog3533.html',
          'http://www.gotoread.com/scatalog3482.html',
          'http://www.gotoread.com/scatalog3477.html'
          ]

    rules = (
        Rule(LinkExtractor(allow=r'/mag/\d+/$'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = MagazineItem()
        i['name'] = sel.xpath("//div[@class='ProName']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@class='content box-line word']").extract()
        i['price'] = sel.xpath("//em/del/text()").extract()[0]
        i['category'] = sel.xpath("//div[@id='DaoHang']/a/text()").extract()[-1]
        imgurl = sel.xpath("//img[@id='magcoverpic']/@src").extract()[0]
        absurl = urlparse.urljoin("http://www.gotoread.com/", imgurl.strip())
        i['image_urls'] = [absurl]
        return i
