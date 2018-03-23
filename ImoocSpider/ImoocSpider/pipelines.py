# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ImoocspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 使用自定义的方式导出json
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()


class JsonItemExporterPipeline(object):
    # 使用 JsonItemExporter 导出json
    def __init__(self):
        self.file = open('article_exporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            item['front_image_path'] = value['path']
        return item


class MysqlPipeline(object):
    # 同步数据插入
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums']))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DATABASE_NAME'],
            user=settings['MYSQL_USERNAME'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用 twisted 将数据插入异步化
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_err, item, spider)
        return item

    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into jobbole_article(title, url, create_date, fav_nums)
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums']))

    def handle_err(self, failure, item, spider):
        pass
