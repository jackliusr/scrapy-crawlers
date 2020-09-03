import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time

class JczqwSpider(scrapy.Spider):
    name = "jczqw"
    
    start_urls = ["http://www.jczqw.com/news/yingchao/index-1.html"]
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }
    def start_requests(self):
        for i in range(1,31):
            yield Request(url=f"http://www.jczqw.com/news/yijia/index-{i}.html", callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        pages = sel.xpath("//div[contains(@class,'zhiboDiv')]/ul/li/a/@href").extract()
        for page in pages:
          yield Request(url = f'http://www.jczqw.com{page}', callback=self.parsePage)

    def parsePage(self,response):
        sel = Selector(response)
        title = ''.join(sel.xpath("//div[@class=\"ah\"]/h1/text()").extract()).strip ()
        content = ''.join(sel.xpath("//div[contains(@class,'ar_body')]").extract()).strip()
        pubTimeTmp = (sel.xpath("//div[@class='ah']/p/span[1]/text()").get())
        pubTime = pubTimeTmp[3:27]
        keywords = sel.xpath("//meta[@name='keywords']/@content").get()
        description = sel.xpath("//meta[@name='description']/@content").get()
        image= sel.xpath("//div[contains(@class,'ar_body')]//img[1]/@src").get()
        category = 2
        if image:
            image_url = image
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
