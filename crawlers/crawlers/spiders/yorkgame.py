from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from crawlers.items import GameItem
from scrapy.http import TextResponse,FormRequest,Request
import json
from scrapy import log

class YorkgameSpider(CrawlSpider):
  
  name = 'yorkgame'
  
  allowed_domains = ['yorkgame.com']
  
  start_urls = ['http://www.yorkgame.com/chinas-game-c-56.html',
		'http://www.yorkgame.com/game-taiwans-game-c-80.html',
		'http://www.yorkgame.com/hong-kong-game-european-game-c-81.html',
		'http://www.yorkgame.com/game-c-86.html',
		'http://www.yorkgame.com/game-activation-code-c-87.html',
		'http://www.yorkgame.com/game-gold-coins-c-85.html',
		'http://www.yorkgame.com/game-accessories-c-84.html',
		'http://www.yorkgame.com/recommended-c-88.html',
		'http://www.yorkgame.com/purchasing-agency-c-83.html',
		'http://www.yorkgame.com/holiday-special-c-83_90.html',
		'http://www.yorkgame.com/mothers-special-c-83_89.html'
		]

  rules = (
      Rule(SgmlLinkExtractor( restrict_xpaths='//div[@class="list_box"]'), callback='parse_item', follow=False),
  )
    
  def parse_item(self, response):
    sel = Selector(response)
    i = GameItem()
    i['name'] = sel.xpath('//div[@id="products_info"]/h1/text()').extract()[0]
    i['description'] =' '.join(sel.xpath('//div[@id="Info_Desc"]/*').extract())
    i['category'] = sel.xpath('//div[@class="headerNavigation"]/a[2]/text()').extract()[0]
    i['price'] = sel.xpath("//div[@class='infoprice']/text()").extract()[0]
    i['image_urls'] = ["http://www.yorkgame.com/" +  sel.xpath("//img[@id='Default_Image']/@src").extract()[0]]
    return i;