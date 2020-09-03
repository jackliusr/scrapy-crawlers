import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time
import re
import w3lib.html
import pprint

class DltSpider(scrapy.Spider):
    name = "dlt"
    
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }
    
    def start_requests(self):
        for i in range(1 , 40):
            yield Request(url =f"https://www.cz89.com/dlt/item_13.htm?p={i}", callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        pages = sel.xpath("//ul[contains(@class,\"listpage\")]//a/@href").getall()
        for page in pages:
            yield Request(url=f"https://www.cz89.com{page}", callback=self.parsePage)
            
    def parsePage(self,response):
        sel = Selector(response)
        p = re.compile(r"<img.*?/?>")
        title = sel.xpath("//div[contains(@class, 'article')]/h5/text()").get()
        content = sel.xpath("//div[@class=\"detail\"]").get()
        content2 = p.sub("", content)
        pubTimeTmp = (sel.xpath("//div[contains(@class, 'article')]/p/text()").get())
        if pubTimeTmp:
            pubTime = pubTimeTmp[4:23].replace(u'\xa0', u' ').strip() 
        else:
            pubTime = "2020-09-01"

        keywords = sel.xpath("//meta[@name='keywords']/@content").get()
        description = sel.xpath("//meta[@name='Description']/@content").get()
        image= sel.xpath("//div[@class='detail']/img[1]/@src").get()
        if not keywords:
            keywords = title
        if not description: 
            description = title

        category = 2
        if image:
            image_url = image
            yield {
                "title": title,
                "content": content2,
                "pubTime": pubTime,
                "keywords": keywords,
                "description": description,
                'category': category,
                "images": [image_url],
                "image_urls": [image_url],
            }
        else:
            yield {
                "title": title,
                "content": content2,
                "pubTime": pubTime,
                "keywords": keywords,
                "description": description,
                'category': category,
            }
