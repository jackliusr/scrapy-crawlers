from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from crawlers.items import EduTrustItem
from scrapy.http import TextResponse,FormRequest,Request
import json
import re
from scrapy import log

class EdutrustSpider(CrawlSpider):
    name = 'edutrust'
    allowed_domains = ['cpe.gov.sg']
    start_urls = ['http://www.cpe.gov.sg/cos/o.x?c=/cpe/peis&ptid=401&func=getedutrust&filterby=&kw=&type=&pg=1',
		  'http://www.cpe.gov.sg/cos/o.x?c=/cpe/peis&ptid=401&func=getedutrust&filterby=&kw=&type=&pg=2',
		  'http://www.cpe.gov.sg/cos/o.x?c=/cpe/peis&ptid=401&func=getedutrust&filterby=&kw=&type=&pg=3'
		  ]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'profile'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = EduTrustItem()
        
        tbl1 = sel.xpath("//table[@class='peiprofile']")[0]
        i['name'] = tbl1.xpath('./tbody/tr[1]/td[1]/text()').extract()
        i['website'] = tbl1.xpath("./tbody/tr[11]/td[1]/a/text()").extract()   
        i['address']=tbl1.xpath("./tbody/tr[7]/td[1]/text()").extract()[0].strip('\n\t ')
        i['phone']= tbl1.xpath("./tbody/tr[8]/td[1]/text()").extract() 
        i['institutionType'] = tbl1.xpath("./tbody/tr[6]/td[1]/text()").extract() 
        
        tbl2 = sel.xpath("//table[@class='peiprofile']")[1]
        i['eduTrustType']=tbl2.xpath('./tbody/tr[2]/td[1]/text()').extract()
        period =tbl2.xpath('./tbody/tr[4]/td[1]/text()').extract()[0].strip('\n\t ')
        i['validityPeriod']= re.sub('\nto\n',' to ', period) 
	i['eduTrustPage'] = response.url;
        return i
