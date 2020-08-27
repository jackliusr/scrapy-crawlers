
import scrapy
from selenium import webdriver
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time
import json

class DemoSpider(scrapy.Spider):
    name = 'hljtycp'
    start_urls = ['https://www.hljtycp.org.cn/newsList/0101']

    def start_requests(self):
       for i in range(1,2):
           data = {"channelNo":"0101","pageIndex":i,"pageSize":20}
           yield JsonRequest(url="https://www.hljtycp.org.cn/hljtcapi/information/list", data=data, callback=self.parseJson)

    def parseJson(self, response):
        resp = json.loads(response.text)
        data = resp["data"]
        pageList = data["informationList"]
        for page in pageList:
            pageId = page["id"]
            yield Request(url=f"https://www.hljtycp.org.cn/newsDetail/0101/{pageId}",callback=self.parsePage)

    def parsePage(self,response):
        sel = Selector(response)
        title = ''.join(sel.xpath("//div[@class=\"n-d-tit\"]//text()").extract()).strip()
        content = ''.join(sel.xpath("//div[@class=\"content-box\"]//text()").extract()).strip()
        pubTime = sel.xpath("//div[@class=\"news-detail_info\"]/span[1]")[0].extract()
        keywords = sel.xpath("//meta[@name='keywords']/@content")[0].extract()
        description = sel.xpath("//meta[@name='description']/@content")[0].extract()
        image= sel.xpath("//div[@class=\"content-box\"]//img[1]/@src")
        image_url =""
        if image:
            image_url = image[0].extract()
        yield {
            "title": title,
            "content": content,
            "pubTime": pubTime,
            "keywords": keywords,
            "description": description,
            "images": image_url,
            "image_urls": image_url,
        }
        
