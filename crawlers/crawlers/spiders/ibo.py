from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor 
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import IboSchoolItem

class IboSpider(CrawlSpider):
    name = 'ibo'
    allowed_domains = ['ibo.org']
    start_urls = ['http://ibo.org/school/search/index.cfm?programmes=&country=SG&region=&find_schools=Find',
          'http://ibo.org/school/search/index.cfm?nextStart=2']

    rules = (
        Rule(LinkExtractor(allow=r'/school/\d*/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = IboSchoolItem()
        i['name'] = sel.xpath("//div[@id='body_right_content_left']/h1/text()").extract()
        return i
