import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time

class Win310Spider(scrapy.Spider):
    name = "win310"
    start_urls = ["https://www.310win.com/jingcaizuqiu/info_t1sub1page1.html"]
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True 
    }
    def start_requests(self):
        for i in range(1,100):
            yield Request(url=f"https://www.310win.com/jingcaizuqiu/info_t1sub1page{i}.html", callback=self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        pages = sel.xpath("//table[@class=\"htbList\"]//a[contains(@href, '.html')]/@href").extract()
        for page in pages:
          yield Request(url = f'https://www.310win.com{page}', callback=self.parsePage)

    def parsePage(self,response):
        sel = Selector(response)
        title = ''.join(sel.xpath("//div[@class='articleTitle']/text()").extract()).strip ()
        content = ''.join(sel.xpath("(//div[@class=\"articleContent\"])[1]//text()").extract()).strip()
        pubTimeTmp = (sel.xpath("//div[@class=\"aInfo\"]/text()").extract_first())
        pubTime = pubTimeTmp[11:27]
        keywords = sel.xpath("//meta[@name='Keywords']/@content").extract_first()
        description = sel.xpath("//meta[@name='Description']/@content").extract_first()
        image= sel.xpath("//div[@class=\"n_zi\"]//img[1]/@src")
        category = 2
        if image:
            image_url = f"https://www.310win.com{image[0].extract()}"
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
