import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlers.items import JdItem
from scrapy.http import TextResponse,FormRequest,Request
import json

class JdMusicSpider(CrawlSpider):
    name = "jd-music"
    allowed_domains = ['jd.com']
    start_urls = ['http://music.jd.com/8_0_desc_7254_2_1_15.html',
          'http://music.jd.com/8_0_desc_7247_2_1_15.html',
          'http://music.jd.com/8_0_desc_7246_2_1_15.html',
          'http://music.jd.com/8_0_desc_7253_2_1_15.html',
          'http://music.jd.com/8_0_desc_7255_2_1_15.html',
          'http://music.jd.com/8_0_desc_7256_2_1_15.html',
          'http://music.jd.com/8_0_desc_7248_2_1_15.html',
          'http://music.jd.com/8_0_desc_7250_2_1_15.html']

    rules = (
      Rule(LinkExtractor(allow=r'music\.jd\.com/\d+.html'), callback='parse_item', follow=False),
    )
      
    def parse_item(self, response):
        sel = Selector(response)
        i = JdItem()
        i['name'] = sel.xpath("//div[@class='product-name']/h1/text()").extract()
        i['description'] = sel.xpath("//div[@class='summary-additional']").extract()[0]
        i['category'] = sel.xpath("//div[@class='breadcrumbs']/a/text()").extract()[3]
        i['price'] = sel.xpath("//span[contains(@class,'price-fore')]/text()").extract()
        i['image_urls'] = sel.xpath("//div[@class='product-image']/img/@data-lazyload").extract()
        return i;
