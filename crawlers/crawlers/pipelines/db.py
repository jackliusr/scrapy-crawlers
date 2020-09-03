import mysql.connector
from scrapy.exceptions import NotConfigured
from datetime import datetime
import random
from dateutil.parser import parse

class DatabasePipeline(object):
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def timestamp(self):
        return int(datetime.now().timestamp())
    def timestamp_safe(self, str):
        return int(parse(str).timestamp())
    def process_item(self, item, spider):
            category = random.randint(1,9)
            title = item['title']
            keywords = item['keywords']
            desc = item['description']
            content = item['content']
            image_url =  ""
            if len(item['images']) > 0:
                image_url = f"/uploads/allimg/{item['images'][0]['path']}"
            ts = self.timestamp_safe(item['pubTime'])
            sr = self.timestamp()
            sql = "insert into dede_arctiny(`typeid`, `typeid2`, `arcrank`, `channel`, `senddate`, `sortrank`, `mid`) values(%s, %s, %s, %s, %s, %s, %s)"
            val = (category, '0', 0, 1, ts, sr, 1)
            self.cursor.execute(sql, val)
            aid = self.cursor.lastrowid
            sql = "INSERT INTO dede_addonarticle VALUES(%s, %s, %s, %s, %s, %s)"
            val = (aid, category, content, '', '', '127.0.0.1')
            self.cursor.execute(sql, val)
            sql = "INSERT INTO dede_archives(" \
                    "id, typeid, sortrank, flag, title, shorttitle, writer, source, litpic, pubdate, senddate, mid, " \
                    "keywords, voteid, description) " \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (aid, category, sr, 'p', title, '', '', '',  image_url, ts, sr, 1, keywords, 0, desc)
            self.cursor.execute(sql, val)

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(db = self.db,
                                 user = self.user, passwd = self.passwd,
                                 host = self.host,
                                 charset = 'utf8', use_unicode = True
                                 )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("DATABASEPIPELINE_ENABLED"):
            raise NotConfigured

        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings: #if we don't define db config in settings
            raise NotConfigured  # then raise an error

        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['password']
        host = db_settings['host']
        return cls(db,user,passwd, host) # return pipeline instance
