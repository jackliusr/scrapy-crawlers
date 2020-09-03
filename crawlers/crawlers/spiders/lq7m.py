
import scrapy
from selenium import webdriver
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time
import json

class Lq7mSpider(scrapy.Spider):
    name = 'lq7m'
    start_urls = ['http://lq.7m.com.cn/list/3/2.shtml']

    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }

    def start_requests(self):
       for i in range(2,200):
           yield Request(url=f"http://lq.7m.com.cn/list/3/{i}.shtml",  callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        urls = sel.xpath("//div[@class=\"cb_l\"]//a[contains(@href, '/news/')]/@href").extract()
        for url in urls:
            yield Request(url=f"http://lq.7m.com.cn{url}",callback=self.parsePage)
    def parsePage(self,response):
        sel = Selector(response)
        title = ''.join(sel.xpath("//div[@class=\"pa_tec\"]/h1/text()").extract()).strip ()
        content = ''.join(sel.xpath("//div[@class=\"n_zi\"]//text()").extract()).strip()
        pubTimeTmp = (sel.xpath("//div[@class=\"pa_tek\"]/div[@class=\"pa_tec\"]/p[1]/text()").extract_first())
        pubTime = pubTimeTmp[15:26] 
        keywords = sel.xpath("//meta[@name='keywords']/@content")[0].extract()
        description = sel.xpath("//meta[@name='description']/@content")[0].extract()
        image= sel.xpath("//div[@class=\"n_zi\"]//img[1]/@src")
        category = 2
        if image:
            image_url = f"http://lq.7m.com.cn{image[0].extract()}"
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
