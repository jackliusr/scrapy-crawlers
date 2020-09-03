import scrapy
from scrapy.http import JsonRequest, Request
from scrapy import Selector
import time

class LotteryRuleSpider(scrapy.Spider):
    name = "lotteryrule"
    start_urls = ["https://www.caipiaokong.com/wanfa/",
             "https://www.caipiaokong.com/shuyu/",
             "https://www.caipiaokong.com/jiqiao/" ]
             
    custom_settings = {
        'DATABASEPIPELINE_ENABLED': True,
    }
    
    def start_requests(self):
        for i in  range(1,9):
            yield Request(url= f"https://www.caipiaokong.com/wanfa/index.php?page={i}", callback=self.parseLink)

    def parseLink(self, response):
        sel = Selector(response)
        pages = sel.xpath("//div[@class='bm']//a[contains(@href, 'article/')]/@href").extract()
        for page in pages:
            yield Request(url = f"https://www.caipiaokong.com/{page}", callback=self.parsePage)

    def parsePage(self,response):
        sel = Selector(response)
        title = sel.css("div.h.hm > h1").extract_first()
        content = sel.xpath("//*[@id=\"article_content\"]").extract_first()
        pubTimeTmp = (sel.xpath("//p[@class='xg1']/text()").extract_first())
        pubTime = "2020-09-01"
        keywords = sel.xpath("//meta[@name='keywords']/@content").extract_first()
        description = sel.xpath("//meta[@name='description']/@content").extract_first()
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
         
