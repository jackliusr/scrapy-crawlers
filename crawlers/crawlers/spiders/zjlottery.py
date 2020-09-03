import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time
import re
import w3lib.html
import pprint


class ZjlotterySpider(scrapy.Spider):
    name = "zjlottery"
    
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }
    
    def start_requests(self):
        for i in range(1,132):
            yield Request(url=f"https://www.zjlottery.com/NewReport/ShowClass.asp?ClassID=68&page={i}", callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        pages = sel.xpath("//div[@class='list']/ul//a/@href").extract()
        for page in pages:
            yield Request(url = f"https://www.zjlottery.com{page}", callback=self.parsePage)

    
    def parsePage(self,response):
        sel = Selector(response)
        p = re.compile(r"<img.*?/?>")
        title = sel.xpath("//div[@class='title']/h1/text()").extract_first()
        content = sel.xpath("//div[@class='content']").extract_first()
        content2 = p.sub("", content)
        pubTimeTmp = (sel.xpath("//div[@class='title']/span/text()").extract_first())
        if pubTimeTmp:
            pubTime = pubTimeTmp[0:19].replace(u'\xa0', u' ').strip() 
        else:
            pubTime = "2020-09-01"

        keywords = sel.xpath("//meta[@name='Keywords']/@content").extract_first()[0:30]
        description = sel.xpath("//meta[@name='Description']/@content").extract_first()
        image= sel.xpath("//div[@class=\"content\"]//img[1]/@src")
        category = 2
        if image:
            image_url = f"https://www.zjlottery.com{image[0].extract()}"
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
         
