# Scrapy-crawlers

Crawlers which I used in different projects. More complex spiders are listed below which crawl ajax dynamic contents.


## jd-children-clothers

use selenium to get dynamically generated contents by javascript (jd using ajax to load price information).  
### How to setup this environment 
http://jackliusr.blogspot.sg/2013/11/scrapy-to-crawl-dynamic-contents.html

Actually there are other solutions to this kind of issues, However at that time I don't find the reason why "Passing additional data to callback functions" don't work. So I worked on other workaround solutions to dynamic content issue. This is one of the solutions. Other solutions are scrapyjs, phantomjs. A big disadvantage of these kind of solutions is very slow as they need to load many other resources such as image, javascript etc. when pages are loading.

I noticed that message "Filtered offsite request to  'p.3.cn'" in scrapy console during one test. I added the domain into allowed_domains and "Passing additional data to callback functions" works

## jd-hardware
Based on BaseSpider

## jd-kitchenware
Based CrawlSpider
