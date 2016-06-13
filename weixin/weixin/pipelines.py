# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime
import copy
import codecs
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MongoDBPipeline(object):
    def __init__(self):
        self.connection_string = "mongodb://%s:%d" % (settings['MONGODB_SERVER'],settings['MONGODB_PORT'])

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        self.log = logging.getLogger(spider.name)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        post_data = copy.deepcopy(item)
        weixin_id_exsist = True if self.collection.find({'weixin_id':item['weixin_id']}).count()>0 else False
        if weixin_id_exsist == False:
            self.collection.insert_one(dict(post_data))
            self.log.debug('weixin_id:%s added to mongdb!'%item['weixin_id'],)
        else:
            if spider.update:
                self.collection.update_one({'weixin_id':item['weixin_id']},{'$set':dict(post_data)})
                self.log.debug('weixin_id:%s exist,update!' %item['weixin_id'])
            else:
                self.log.debug('weixin_id:%s exist,not update!' %item['weixin_id'])

        return item


    def __process_html(self,item):
        if item['html'] == None or item['html'] == '':
            self.log.debug('the weixinid:%s html body is empty!'%item['weixin_id'])
            return False
        item['html'] = re.sub(r'<link href=\"/css/style\.css','<link href=\"css/style.css',item['html'])
        #deal script
        item['html'] = re.sub(r'<script src=\"https://static\.weixin\.org/static/js/jquery\-1\.4\.2\.min\.js','<script src=\"js/jquery-1.4.2.min.js',item['html'])
        return True
