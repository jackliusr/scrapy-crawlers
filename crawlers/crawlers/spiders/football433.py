import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time
import json

class Football433Spider(scrapy.Spider):
    name = "football433"
    start_urls = ["https://www.310win.com/jingcaizuqiu/info_t1sub1page1.html"]
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': False 
    }
    def start_requests(self):
        for i in range(1,2):
            yield scrapy.FormRequest(url=f"https://www.433.com/xxs/xxslistmore", formdata={'types':'5','p': f"{i}"}, callback=self.parseList)

    def parseList(self, response):
        jsonresp = json.loads(response.text)
        for page in jsonresp:
          yield Request(url = f'https://www.433.com/qingbao/{page["Id"]}-{page["MatchId"]}.html', callback=self.parsePage)

    def parsePage(self,response):
        sel = Selector(response)
        title = ''.join(sel.xpath("//h1[contains(@class,\"ptitname\")]/text()").extract()).strip ()
        content = ''.join(sel.xpath("//div[@class='cprteamdata']/div[2]").get()).strip()
        # pubTimeTmp = (sel.xpath("//div[@class=\"aInfo\"]/text()").extract_first())
        pubTime = "2020-09-01"
        keywords = sel.xpath("//meta[@name='keywords']/@content").extract_first()
        description = sel.xpath("//meta[@name='description']/@content").extract_first()
        image= sel.xpath("//div[@class='cprteamdata']/div[2]//img[1]/@src").get()
        category = 2
        if image:
            image_url = f"https://www.433.com{image[0].extract()}"
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
