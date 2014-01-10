from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from crawlers.items import GameItem
from scrapy.http import TextResponse,FormRequest,Request
import json
from scrapy import log

class KaletouSpider(CrawlSpider):
    name = 'kaletou'
    allowed_domains = ['kaletou.com']
    #start_urls = ['http://www.kaletou.com/']

    start_urls = ['http://www.kaletou.com/category.php?id=13',
		  'http://www.kaletou.com/category.php?id=17',
		  'http://www.kaletou.com/category.php?id=159',
		  'http://www.kaletou.com/category.php?id=160',
		  'http://www.kaletou.com/category.php?id=161',
		  'http://www.kaletou.com/category.php?id=162',
		  'http://www.kaletou.com/category.php?id=1',
		  'http://www.kaletou.com/category.php?id=5',
		  'http://www.kaletou.com/category.php?id=49',
		  'http://www.kaletou.com/category.php?id=163',
		  'http://www.kaletou.com/category.php?id=164',
		  'http://www.kaletou.com/category.php?id=165',
		  'http://www.kaletou.com/category.php?id=14',
		  'http://www.kaletou.com/category.php?id=25',
		  'http://www.kaletou.com/category.php?id=29',
		  'http://www.kaletou.com/category.php?id=92',
		  'http://www.kaletou.com/category.php?id=34',
		  'http://www.kaletou.com/category.php?id=166',
		  'http://www.kaletou.com/category.php?id=167',
		  'http://www.kaletou.com/category.php?id=2',
		  'http://www.kaletou.com/category.php?id=3',
		  'http://www.kaletou.com/category.php?id=4',
		  'http://www.kaletou.com/category.php?id=6',
		  'http://www.kaletou.com/category.php?id=15',
		  'http://www.kaletou.com/category.php?id=16',
		  'http://www.kaletou.com/category.php?id=18',
		  'http://www.kaletou.com/category.php?id=19',
		  'http://www.kaletou.com/category.php?id=20',
		  'http://www.kaletou.com/category.php?id=22',
		  'http://www.kaletou.com/category.php?id=23',
		  'http://www.kaletou.com/category.php?id=24',
		  'http://www.kaletou.com/category.php?id=26',
		  'http://www.kaletou.com/category.php?id=27',
		  'http://www.kaletou.com/category.php?id=28',
		  'http://www.kaletou.com/category.php?id=30',
		  'http://www.kaletou.com/category.php?id=35',
		  'http://www.kaletou.com/category.php?id=36',
		  'http://www.kaletou.com/category.php?id=37',
		  'http://www.kaletou.com/category.php?id=40',
		  'http://www.kaletou.com/category.php?id=41',
		  'http://www.kaletou.com/category.php?id=45',
		  'http://www.kaletou.com/category.php?id=48',
		  'http://www.kaletou.com/category.php?id=50',
		  'http://www.kaletou.com/category.php?id=51',
		  'http://www.kaletou.com/category.php?id=54',
		  'http://www.kaletou.com/category.php?id=55',
		  'http://www.kaletou.com/category.php?id=57',
		  'http://www.kaletou.com/category.php?id=61',
		  'http://www.kaletou.com/category.php?id=64',
		  'http://www.kaletou.com/category.php?id=70',
		  'http://www.kaletou.com/category.php?id=80',
		  'http://www.kaletou.com/category.php?id=87',
		  'http://www.kaletou.com/category.php?id=90',
		  'http://www.kaletou.com/category.php?id=97',
		  'http://www.kaletou.com/category.php?id=114',
		  'http://www.kaletou.com/category.php?id=115',
		  'http://www.kaletou.com/category.php?id=121',
		  'http://www.kaletou.com/category.php?id=129',
		  'http://www.kaletou.com/category.php?id=155',
		  'http://www.kaletou.com/category.php?id=168',
		  'http://www.kaletou.com/category.php?id=170',
		  'http://www.kaletou.com/category.php?id=174'
		  ]

    rules = (
	Rule(SgmlLinkExtractor(allow=r'goods\.php\?id='), callback='parse_item', follow=False),
    )
      
    def parse_item(self, response):
      sel = Selector(response)
      i = GameItem()
      i['name'] = sel.xpath("//div[@id='content']/div/div[1]/div[1]/div[2]/h1/text()").extract()[0]
      i['description'] = ' '.join(sel.xpath("//div[@id='description']/div[2]/div/*").extract())
      cntLinks = sel.xpath("//p[@class='breadcrumbs']/a")
      if len(cntLinks) >2:
	i['category'] = sel.xpath("//p[@class='breadcrumbs']/a[3]/text()").extract()[0]
      else:
	i['category'] = i['name']
      
      i['price'] = sel.xpath("//form[@id='purchase_form']/ul/li[1]/em/text()").extract()[0]
      i['image_urls'] = ["http://www.kaletou.com/" +  sel.xpath("//div[@id='gallery']/a/img/@src").extract()[0]]
      return i;

