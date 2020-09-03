import scrapy
from scrapy.http import JsonRequest,Request 
from scrapy import Selector
import time

class Spbo1Spider(scrapy.Spider):
    name = "spbo1"
    start_urls = ["http://sports.spbo1.com/s/football/zc/list_19_1.html"]
    
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }

    def start_requests(self):
        for i in range(1,200):
            yield Request(url=f"http://sports.spbo1.com/s/football/zc/list_19_{i}.html",callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        pages = sel.xpath("//div[@class=\"box\"]/ul/li/a[1]/@href").extract()
        for page in pages:
            yield Request(url = f"http://sports.spbo1.com{page}", callback=self.parsePage)

    def parsePage(self, response):
        sel = Selector(response)
        title = ''.join(sel.xpath("//div[@class=\"CLbodytitle\"]/h1/text()").extract()).strip ()
        content = ''.join(sel.xpath("//div[@class=\"CLartibody\"]//text()").extract()).strip()
        pubTimeTmp = (sel.xpath("//div[@class=\"CLfinfo\"]/text()").extract_first())
        pubTime = pubTimeTmp[22:38]
        keywords = sel.xpath("//meta[@name='keywords']/@content").extract_first()
        description = sel.xpath("//meta[@name='description']/@content").extract_first()
        image= sel.xpath("//div[@class=\"CLblkzw\"]//img[1]/@src")
        category = 2
        if image:
            image_url = f"http://sports.spbo1.com{image[0].extract()}"
            yield {
                "title": title,
                "content": content,
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
                "content": content,
                "pubTime": pubTime,
                "keywords": keywords,
                "description": description,
                'category': category,
            }
