# Scrapy settings for crawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawlers'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlers (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline':10,
    'crawlers.pipelines.db.DatabasePipeline': 20,
    }

DOWNLOAD_DELAY = 1

"""
DOWNLOADER_MIDDLEWARES = {
    'scrapyjs.middleware.WebkitDownloader': 1,
}
"""

IMAGES_STORE = '/app/images/'

DB_SETTINGS = {
    'db': 'dedecmsv57utf8sp2',
    'user': 'root',
    'password': 'HbLOA5VZK2aUOiBIfLRl',
    'host': '172.18.0.2'
}
