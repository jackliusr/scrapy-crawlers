
import scrapy
from selenium import webdriver

class DemoSpider(scrapy.Spider):
    name = 'demo'
    start_urls = ['http://quotes.toscrape.com/js']

    def __init__(self, *args, **kwargs):
        super(DemoSpider, self).__init__(*args, **kwargs)

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
    
    def parse(self, response):
        self.driver.get(response.url)
        for quote in self.driver.find_elements_by_css_selector('div.quote'):
            yield {
                'quote': quote.find_element_by_css_selector('span').text,
                'author': quote.find_element_by_css_selector('small').text,
            }
        next_page_url = response.css('nav li.next a ::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))