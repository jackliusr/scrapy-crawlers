import scrapy
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
'''
遇到不懂的问题？Python学习交流群：821460695满足你的需求，资料都已经上传群文件，可以自行下载！
'''
class ToutiaoExampleSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    start_urls = ['https://www.toutiao.com/api/pc/focus/'] ###今日头条焦点的api接口
    def parse(self, response):
        conten_json=json.loads(response.text)
        conten_news=conten_json['data'] ###从json数据中抽取data字段数据，其中data字段数据里面包含了pc_feed_focus这个字段，其中这个字段包含了：新闻的标题title，链接url等信息
        for aa in  conten_news['pc_feed_focus']:
            title=aa['title']
            link_url='https://www.toutiao.com'+aa['display_url'] ###如果写（www.toutiao.com'+aa['display_url']）会报错，加上https://,(https://www.toutiao.com'+aa['display_url'])则不会报错！
            link_url_new=link_url.replace('group/','a')###把链接https://www.toutiao.com/group/6574248586484122126/，放到浏览器中，地址会自动变成https://www.toutiao.com/a6574248586484122126/这个。所以我们需要把group/ 替换成a

            yield scrapy.Request(link_url_new, callback=self.next_parse)

    def next_parse(self, response):

        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置useragent信息
        dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ')  # 根据需要设置具体的浏览器信息
        driver = webdriver.PhantomJS(desired_capabilities=dcap)  #封装浏览器信息) # 指定使用的浏览器,

        #driver.set_page_load_timeout(5)  # 设置超时时间
        driver.get(response.url)##使用浏览器请求页面

        time.sleep(3)#加载3秒，等待所有数据加载完毕


        title=driver.find_element_by_class_name('title').text  ###.text获取元素的文本数据
        content1=driver.find_element_by_class_name('abstract-index').text###.text获取元素的文本数据
        content2=driver.find_element_by_class_name('abstract').text###.text获取元素的文本数据

        content=content1+content2

        print(title,content,6666666666666666)
        driver.close()

      #data = driver.page_source# 获取网页文本
      #driver.save_screenshot('1.jpg')  # 系统截图保存
