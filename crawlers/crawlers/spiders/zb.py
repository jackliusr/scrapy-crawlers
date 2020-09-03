import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time
import re
import w3lib.html
import pprint

class ZbSpider(scrapy.Spider):
    name = "zb"
    
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }
    
    def start_requests(self):
        for i in range(1 , 40):
            yield Request(url =f"https://zx.55128.cn/csxw/list/110_{i}.htm", callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        pages = sel.xpath("//ul[@id='loadList']//a/@href").getall()
        for page in pages:
            yield Request(url=f"https://zx.55128.cn{page}", callback=self.parsePage)
            
    def parsePage(self,response):
        sel = Selector(response)
        p = re.compile(r"<img.*?/?>")
        title = sel.xpath("//div[@class='title']/h1/text()").get()
        content = sel.xpath("//div[contains(@class,'article')]").get()
        if not content:
            return;

        content2 = p.sub("", content)
        pubTimeTmp = (sel.xpath("//div[@id='txt']/div[@class='author']/text()").get())
        if pubTimeTmp:
            pubTime = pubTimeTmp[-10:].replace(u'\xa0', u' ').strip() 
        else:
            pubTime = "2020-09-01"

        keywords = title
        description = title
        image= sel.xpath("//div[contains(@class,'article')]//img[1]/@src").get()
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
