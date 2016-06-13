# -*- coding: utf-8 -*-
from datetime import datetime
import pymongo
import scrapy
from weixin.items import weixinItem
from scrapy.conf import settings
from scrapy.contrib.spiders import CrawlSpider,Rule
import re


class weixinSpider(CrawlSpider):
    name = "weixin"
    allowed_domains = ["mp.weixin.qq.com"]
    start_urls = ['http://weixin.sogou.com/pcindex/pc/pc_0/1.html']

    def __init__(self,page_max=settings['PAGE_MAX_DEFAULT'],local_store=settings['LOCAL_STORE_DEFAULT'],\
            update=settings['UPDATE_DEFAULT'],*args, **kwargs):
        self.page_max = int(page_max)
        self.local_store = 'true' == local_store.lower()
        self.update = 'true' == update.lower()

        self.connection_string = "mongodb://%s:%d" % (settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def closed(self,reason):
        self.client.close()

    def parse(self, response):
        total_pages = int('5')
        if self.page_max == 0:
            end_page = int(total_pages)
        else:
            end_page = self.page_max

        #翻页
        curpage=int(re.findall('\d+',response.url)[-1])
        if curpage<end_page:
            nextpage=re.sub('/\d+\.html','/%d.html'%(curpage+1),response.url)
            yield scrapy.Request(nextpage, self.parse)

        print response.xpath('//div[@class="pos-wxrw"]/a/@href').extract()[0]
        for x in response.xpath('//div[@class="pos-wxrw"]'):
            item = weixinItem()
            item['html'] = x.xpath('a/@href').extract()[0]
            yield scrapy.Request(item['html'], self.parse_detail,meta={'item':item})

    def parse_detail(self,response):
        item=response.meta['item']

        item['weixin_id'] = re.findall('\S+',response.xpath('//p[@class="profile_account"]/text()').extract()[0].split(':')[-1])[0]
        item['author'] = response.xpath("//strong[@class='profile_nickname']/text()").re('\S+')[0]
        item['gongzhonghao_type'] = response.xpath('//div[@class="profile_desc_value"]/@title').extract()[0]
        #print item['author']
        #print item['gongzhonghao_type']

        yield item

    def __search_mongodb(self,weixin_id):

        weixin_id_exsist = True if self.collection.find({'weixin_id':weixin_id}).count()>0 else False

        return weixin_id_exsist


